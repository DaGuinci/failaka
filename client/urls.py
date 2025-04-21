# filepath: /media/DATA/sensei-1000/Documents/1_work/1_dev/Florent/app/failalka/client/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
]