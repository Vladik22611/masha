from django import forms
from django.core.validators import MaxValueValidator


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        label="Введите количество товара",
        min_value=1,  # Минимальное значение 1
        max_value=None,  # Будем задавать максимальное значение динамически
        error_messages={
            "required": "Это поле обязательно для заполнения.",
            "min_value": "Количество должно быть не менее 1.",
            "max_value": "Количество не может превышать {value}.",  # place-holder для значения
        },
        widget=forms.NumberInput(
            attrs={"class": "wide single-input"}
        ),
    )

    def __init__(self, *args, **kwargs):
        count_max = kwargs.pop("count_max", None)  # Получаем значение count_max
        super().__init__(*args, **kwargs)
        if count_max is not None:
            self.fields["quantity"].validators.append(MaxValueValidator(count_max))
            self.fields["quantity"].error_messages[
                "max_value"
            ] = f"Количество не может превышать {count_max}."
