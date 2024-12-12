from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from globals import cursor, conn


class Cart(models.Model):
    """Модель корзины, которая хранит информацию о пользователе."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart"
    )  # Связь с моделью User
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания корзины
    updated_at = models.DateTimeField(
        auto_now=True
    )  # Дата последнего обновления корзины

    def __str__(self):
        return f"Cart of {self.user.username}"

    def clear_cart(self):
        """Очищает корзину пользователя."""
        self.items.all().delete()  # Удаление всех элементов корзины


class CartItem(models.Model):
    """Модель для представления элемента корзины."""

    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE
    )  # Связь с корзиной
    part_number = models.CharField(
        max_length=50, default="PN001"
    )  # Идентификатор продукта (номер детали)
    quantity = models.PositiveIntegerField(default=1)  # Количество продукта в корзине
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Цена на момент добавления в корзину

    # def __str__(self):
    #    return f"{self.part_number}"

    @property
    def total_price(self):
        """Возвращает полную цену за данный товар в корзине."""
        return self.price * self.quantity
