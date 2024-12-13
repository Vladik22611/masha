from django.urls import path

from . import views

urlpatterns = [
    path("delete/order", views.del_order, name="del_order"),
    path("change/order", views.change_order, name="change_order"),
    path("change/order/<int:pk>", views.change_order_def, name="change_order_def"),
    path("change/order/<int:pk>/<slug:part_number>", views.change_order_def_next, name="change_order_def_next"),
    path("add/part", views.add_part, name="add_part"),
    path("delete/part", views.del_part, name="del_part"),
    path("change/part", views.change_part, name="change_part"),
    path("change/part/<slug:pk>", views.change_part_def, name="change_part_def"),
]
