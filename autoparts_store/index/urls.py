from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("order_detail/<int:pk>", views.order_detail,name="order_detail")
]
