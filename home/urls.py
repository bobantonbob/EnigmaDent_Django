from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('prices/', views.prices, name='prices'),
    path('stomatologiya-kyiv/', views.dentistry_kyiv, name='dentistry_kyiv'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('about/', views.about, name='about'),
    path('reviews/', views.google_reviews, name='google_reviews'),
    path('contacts/', views.contacts, name='contacts'),
    path('response/', views.response_create, name='response_create'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('public-contract/', views.public_contract, name='public_contract'),
    path('license/', views.licens, name='licens'),
    path('certificates/', views.certificates, name='certificates'),
]
