from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_list, name='home'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
]