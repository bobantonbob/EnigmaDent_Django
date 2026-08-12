from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('certificate', certificate),
    path('new1', new1),
    path('new2', new2),
    path('new3', new3),

]