from django.urls import path
from . import views

urlpatterns = [
    path('urlshortner/',views.urlshortener),
    path('<str:short_code>/', views.geturl),
    path('',views.dashboard)
]