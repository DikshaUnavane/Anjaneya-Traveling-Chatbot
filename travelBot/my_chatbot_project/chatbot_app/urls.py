# chatbot_app/urls.py

# chatbot_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),

]

