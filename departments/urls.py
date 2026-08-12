from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='departments'),
    path('therapy/', views.therapeutic, name='therapeutic'),
    path('periodontology/', views.periodontology, name='periodontology'),
    path('orthopedics/', views.orthopedic, name='orthopedic'),
    path('appointment/', views.create, name='create'),
]
