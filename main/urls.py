from django.urls import path, include
from . import views

urlpatterns = [
    path('vendors/', views.vendor_list),
    path('vendors/<str:vendor_id>/', views.vendor_detail),
    path('vendors/<str:vendor_id>/performance', views.vendor_performance),

    path("purchase_orders/", views.po_list),
    path("purchase_orders/<str:po_id>/", views.po_detail),
    path("purchase_orders/<str:po_id>/acknowledge", views.add_acknowledgement),
]
