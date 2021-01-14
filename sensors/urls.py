from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('heartbeat', views.heartbeat, name='heartbeat')
]
