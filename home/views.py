from django.contrib import messages
from django.core.paginator import Paginator
from django.db.utils import OperationalError, ProgrammingError
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ResponseForm
from .models import GoogleReview, GoogleReviewStats, PriceCategory, PriceItem, Response
from .services import get_client_ip, notify_telegram
from elements.models import Certificate


def index(request):
    reviews = Response.objects.filter(status=Response.ModerationStatus.APPROVED)[:3]
    google_stats = GoogleReviewStats.objects.filter(pk=1).first()
    google_reviews = GoogleReview.objects.filter(is_visible=True)[:6]
    highlight_codes = ['114', '118', '144', '210', '216', '218', '310', '330', '332']
    highlight_qs = PriceItem.objects.filter(is_active=True, code__in=highlight_codes).select_related('category')
    highlights = {item.code: item for item in highlight_qs}
    return render(request, 'home/index.html', {
        'title': 'Стоматологія у Києві — Enigma Dent',
        'meta_description': 'Enigma Dent — стоматологічний кабінет у Києві: лікування зубів, реставрації, ендодонтія, професійна гігієна, пародонтологія, коронки та протезування. Актуальні ціни й онлайн-запис.',
        'page': 'home',
        'reviews': reviews,
        'google_reviews': google_reviews,
        'google_rating': google_stats.average_rating if google_stats else None,
        'google_rating_count': google_stats.total_review_count if google_stats else None,
        'google_maps_uri': google_stats.google_maps_url if google_stats else '',
        'google_last_sync': google_stats.last_sync_at if google_stats else None,
        'therapy_restore': highlights.get('114'),
        'therapy_front': highlights.get('118'),
        'therapy_fluoride': highlights.get('144'),
        'perio_clean': highlights.get('210'),
        'perio_whitening': highlights.get('216'),
        'perio_vector': highlights.get('218'),
        'ortho_metal': highlights.get('310'),
        'ortho_emax': highlights.get('330'),
        'ortho_implant': highlights.get('332'),
    })


def prices(request):
    categories = PriceCategory.objects.filter(is_active=True).prefetch_related('items')
    grouped = {
        'therapy': [c for c in categories if c.section == PriceCategory.Section.THERAPY],
        'periodontology': [c for c in categories if c.section == PriceCategory.Section.PERIODONTOLOGY],
        'orthopedics': [c for c in categories if c.section == PriceCategory.Section.ORTHOPEDICS],
    }
    return render(request, 'home/prices.html', {
        'title': 'Ціни на стоматологічні послуги у Києві',
        'meta_description': 'Актуальний прайс Enigma Dent: терапевтична стоматологія, лікування каналів, реставрації, професійна чистка, Vector-терапія, коронки, E-max, цирконій та протезування.',
        'page': 'prices',
        'price_groups': grouped,
    })


def contacts(request):
    return render(request, 'home/contacts.html', {'title': 'Контакти', 'page': 'contacts'})


def about(request):
    approved = Response.objects.filter(status=Response.ModerationStatus.APPROVED)
    paginator = Paginator(approved, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Google reviews are stored locally and displayed from our database.
    # Until Google Business Profile API access is approved, this block simply
    # shows the prepared integration state without breaking the page.
    try:
        google_stats = GoogleReviewStats.objects.filter(pk=1).first()
        google_reviews = GoogleReview.objects.filter(is_visible=True)[:6]
    except (OperationalError, ProgrammingError):
        google_stats = None
        google_reviews = []

    return render(request, 'home/about.html', {
        'title': 'Про Enigma Dent',
        'page': 'about',
        'all_response': approved,
        'rows_count': approved.count(),
        'page_obj': page_obj,
        'google_reviews': google_reviews,
        'google_rating': google_stats.average_rating if google_stats else None,
        'google_rating_count': google_stats.total_review_count if google_stats else None,
        'google_maps_uri': google_stats.google_maps_url if google_stats else '',
        'google_last_sync': google_stats.last_sync_at if google_stats else None,
    })


def response_create(request):
    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.ip_address = get_client_ip(request)
            review.save()
            notify_telegram(
                '⭐ <b>Новий відгук Enigma Dent</b>\n'
                f'👤 {review.name}\n'
                f'✉️ {review.email or "не вказано"}\n'
                f'💬 {review.response[:900]}\n'
                '🛡 Статус: очікує модерації в Django Admin'
            )
            messages.success(request, 'Дякуємо! Відгук збережено та передано адміністратору на модерацію.')
            return redirect('response_create')
    else:
        form = ResponseForm()

    return render(request, 'home/response_create.html', {
        'title': 'Залишити відгук',
        'page': 'review',
        'form': form,
    })




def google_reviews(request):
    reviews_qs = GoogleReview.objects.filter(is_visible=True)
    rating = request.GET.get('rating')
    if rating in {'1', '2', '3', '4', '5'}:
        reviews_qs = reviews_qs.filter(star_rating=int(rating))
    paginator = Paginator(reviews_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    stats = GoogleReviewStats.objects.filter(pk=1).first()
    return render(request, 'home/google_reviews.html', {
        'title': 'Відгуки пацієнтів Enigma Dent у Google',
        'meta_description': 'Реальні відгуки пацієнтів Enigma Dent з Google Business Profile: оцінки, коментарі та актуальний рейтинг стоматології у Києві.',
        'page': 'reviews',
        'page_obj': page_obj,
        'google_stats': stats,
        'rating_filter': rating or '',
    })

def privacy_policy(request):
    return render(request, 'home/privacy_policy.html', {'title': 'Політика конфіденційності', 'page': 'legal'})


def public_contract(request):
    return render(request, 'home/public_contract.html', {'title': 'Публічний договір', 'page': 'legal'})



def certificates(request):
    # The static certificate gallery must remain available even before the
    # Certificate migration has been applied on a new/local database.
    try:
        certificates = list(Certificate.objects.filter(is_active=True))
    except (OperationalError, ProgrammingError):
        certificates = []

    return render(request, 'home/certificates.html', {
        'title': 'Сертифікати',
        'page': 'certificates',
        'certificates': certificates,
        'certificate_files': [f'c{i}.jpg' for i in range(1, 12)] if not certificates else [],
    })

def licens(request):
    return render(request, 'home/licens.html', {'title': 'Ліцензія', 'page': 'legal'})




def dentistry_kyiv(request):
    categories = PriceCategory.objects.filter(is_active=True).prefetch_related('items')
    return render(request, 'home/dentistry_kyiv.html', {
        'title': 'Стоматологія у Києві на Нивках',
        'meta_description': 'Стоматологічний кабінет Enigma Dent у Києві, вул. Данила Щербаківського, 72. Терапія, пародонтологія, професійна гігієна, реставрації, коронки та протезування.',
        'page': 'dentistry_kyiv',
        'categories': categories,
    })


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
    ]
    return HttpResponse('\\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    paths = ['', '/departments/', '/prices/', '/stomatologiya-kyiv/', '/about/', '/reviews/', '/certificates/', '/license/', '/contacts/']
    urls = ''.join(f'<url><loc>{settings.SITE_URL}{path}</loc></url>' for path in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return HttpResponse(xml, content_type='application/xml')
