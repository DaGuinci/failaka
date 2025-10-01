from django.urls import path
from . import views

urlpatterns = [
    path('', views.items_list, name='home'),
    path('items/<uuid:item_uuid>/', views.item_detail, name='item_detail'),
    path('sites/', views.sites_list, name='sites_list'),
    path('sites/<uuid:site_uuid>/', views.site_detail, name='site_detail'),
]