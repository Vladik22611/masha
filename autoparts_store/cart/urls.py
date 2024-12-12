from django.urls import path

from . import views

urlpatterns = [
    path("add_order/", views.add_order, name="add_order"),
    path("<slug:art>", views.add_cart, name="add_cart"),
    path("cart/", views.view_cart, name="view_cart"),  # URL для отображения корзины
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),  # URL для удаления элемента из корзины
    
]
