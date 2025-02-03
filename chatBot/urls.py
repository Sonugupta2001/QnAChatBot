from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_document'),
    path('chat/', views.chat, name='chat'),
    path('clear_session/', views.clear_session, name='clear_session'),
]