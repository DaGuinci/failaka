from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
]