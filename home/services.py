import json
import logging
from urllib import parse, request

from django.conf import settings

logger = logging.getLogger(__name__)


def get_client_ip(http_request):
    forwarded = http_request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return http_request.META.get('REMOTE_ADDR')


def notify_telegram(text):
    """Send a Telegram message without making a failed notification break the website form."""
    if not getattr(settings, 'TELEGRAM_NOTIFICATIONS_ENABLED', True):
        return False

    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    if not token or not chat_id:
        logger.info('Telegram notification skipped: credentials are not configured.')
        return False

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = parse.urlencode({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': 'true',
    }).encode('utf-8')

    try:
        req = request.Request(url, data=payload, method='POST')
        with request.urlopen(req, timeout=4) as response:
            return 200 <= response.status < 300
    except Exception:
        logger.exception('Telegram notification failed.')
        return False
