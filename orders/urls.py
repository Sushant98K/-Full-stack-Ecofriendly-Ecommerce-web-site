from django.urls import path
from . import views

urlpatterns = [
    path('order-now/', views.order_now, name='order_now'),
    path('order-submit/', views.order_submit, name='order_submit'),
    path("my-orders/", views.my_orders_view, name="my_orders"),
]
