from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create', views.create, name='create'),
    path('messages', views.messages, name='messages'),
    path('events', views.events, name='events'),
    path('about', views.about, name='about'),
]
