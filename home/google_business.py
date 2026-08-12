import json
import logging
from urllib import parse, request

from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import GoogleReview, GoogleReviewStats

logger = logging.getLogger(__name__)

STAR_MAP = {
    'ONE': 1,
    'TWO': 2,
    'THREE': 3,
    'FOUR': 4,
    'FIVE': 5,
}


def _stats():
    obj, _ = GoogleReviewStats.objects.get_or_create(pk=1)
    return obj


def _post_form(url, payload):
    data = parse.urlencode(payload).encode('utf-8')
    req = request.Request(url, data=data, method='POST', headers={'Accept': 'application/json'})
    with request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def _get_json(url, access_token):
    req = request.Request(url, method='GET', headers={
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    })
    with request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode('utf-8'))


def refresh_access_token():
    client_id = getattr(settings, 'GOOGLE_GBP_CLIENT_ID', '')
    client_secret = getattr(settings, 'GOOGLE_GBP_CLIENT_SECRET', '')
    refresh_token = getattr(settings, 'GOOGLE_GBP_REFRESH_TOKEN', '')
    if not all((client_id, client_secret, refresh_token)):
        raise RuntimeError('Google Business Profile OAuth credentials are not configured yet.')
    payload = _post_form('https://oauth2.googleapis.com/token', {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    })
    token = payload.get('access_token')
    if not token:
        raise RuntimeError(f'Google OAuth did not return access_token: {payload}')
    return token


def discover_accounts(access_token):
    return _get_json('https://mybusinessaccountmanagement.googleapis.com/v1/accounts', access_token)


def discover_locations(access_token, account_name):
    parent = account_name if account_name.startswith('accounts/') else f'accounts/{account_name}'
    fields = 'name,title,storeCode,metadata,phoneNumbers,websiteUri,storefrontAddress'
    url = f'https://mybusinessbusinessinformation.googleapis.com/v1/{parent}/locations?readMask={parse.quote(fields)}&pageSize=100'
    return _get_json(url, access_token)


def _normalize_review(item):
    reviewer = item.get('reviewer') or {}
    reply = item.get('reviewReply') or {}
    rating_raw = item.get('starRating')
    if isinstance(rating_raw, int):
        rating = rating_raw
    else:
        rating = STAR_MAP.get(str(rating_raw or '').upper(), 0)
    review_name = item.get('name', '')
    review_id = review_name.rsplit('/', 1)[-1] if review_name else item.get('reviewId', '')
    return {
        'google_review_id': review_id or review_name,
        'reviewer_name': reviewer.get('displayName') or 'Користувач Google',
        'reviewer_profile_photo_url': reviewer.get('profilePhotoUrl') or '',
        'star_rating': rating or 5,
        'comment': item.get('comment') or '',
        'create_time': parse_datetime(item.get('createTime', '')) if item.get('createTime') else None,
        'update_time': parse_datetime(item.get('updateTime', '')) if item.get('updateTime') else None,
        'reply_comment': reply.get('comment') or '',
        'reply_update_time': parse_datetime(reply.get('updateTime', '')) if reply.get('updateTime') else None,
        'raw_json': item,
    }


def import_reviews_payload(payload, google_maps_url=''):
    created = updated = 0
    for item in payload.get('reviews', []):
        values = _normalize_review(item)
        review_id = values.pop('google_review_id')
        if not review_id:
            continue
        _, was_created = GoogleReview.objects.update_or_create(
            google_review_id=review_id,
            defaults=values,
        )
        created += int(was_created)
        updated += int(not was_created)

    stats = _stats()
    avg = payload.get('averageRating')
    total = payload.get('totalReviewCount')
    if avg is not None:
        stats.average_rating = avg
    if total is not None:
        stats.total_review_count = total
    elif payload.get('reviews') is not None:
        stats.total_review_count = GoogleReview.objects.count()
    if google_maps_url:
        stats.google_maps_url = google_maps_url
    stats.last_sync_at = timezone.now()
    stats.last_sync_status = 'ok'
    stats.last_sync_error = ''
    stats.save()
    return {'created': created, 'updated': updated, 'total': stats.total_review_count}


def sync_google_business_reviews():
    """Synchronize all reviews for the configured verified Enigma Dent location.

    This remains dormant until Google approves GBP API access and OAuth values are
    placed in .env. Reviews are persisted locally, so the website never depends on
    Google being reachable during a page view.
    """
    account_id = getattr(settings, 'GOOGLE_GBP_ACCOUNT_ID', '')
    location_id = getattr(settings, 'GOOGLE_GBP_LOCATION_ID', '')
    if not account_id or not location_id:
        raise RuntimeError('GOOGLE_GBP_ACCOUNT_ID and GOOGLE_GBP_LOCATION_ID are not configured yet.')

    access_token = refresh_access_token()
    account = account_id.replace('accounts/', '')
    location = location_id.replace('locations/', '').split('/')[-1]
    base = f'https://mybusiness.googleapis.com/v4/accounts/{parse.quote(account)}/locations/{parse.quote(location)}/reviews'
    all_reviews = []
    page_token = ''
    average_rating = None
    total_review_count = None
    while True:
        params = {'pageSize': 50, 'orderBy': 'updateTime desc'}
        if page_token:
            params['pageToken'] = page_token
        payload = _get_json(base + '?' + parse.urlencode(params), access_token)
        all_reviews.extend(payload.get('reviews', []))
        average_rating = payload.get('averageRating', average_rating)
        total_review_count = payload.get('totalReviewCount', total_review_count)
        page_token = payload.get('nextPageToken', '')
        if not page_token:
            break

    result = import_reviews_payload({
        'reviews': all_reviews,
        'averageRating': average_rating,
        'totalReviewCount': total_review_count,
    }, getattr(settings, 'GOOGLE_GBP_MAPS_URL', ''))
    return result


def mark_sync_error(exc):
    stats = _stats()
    stats.last_sync_at = timezone.now()
    stats.last_sync_status = 'error'
    stats.last_sync_error = str(exc)[:4000]
    stats.save()
