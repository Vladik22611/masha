from django import forms
from globals import conn, cursor
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator

class DelOrderForm(forms.Form):
    conn.rollback()
    query1 = """
    SELECT order_id FROM orders;
    """
    cursor.execute(query1)
    id_order_mas = cursor.fetchall()
    id_order = forms.ChoiceField(
        label="ID заказа",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_race
        self.fields["id_order"].choices = [(x[0], x[0]) for x in self.id_order_mas]


class ChoicePartNumberForm(forms.Form):
    conn.rollback()

    part_number = forms.ChoiceField(
        label="Выберите артикул из вашего заказа",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        cursor.execute(
            f"SELECT part_number FROM ordered_parts WHERE order_id={self.pk}"
        )
        self.id_order_mas = cursor.fetchall()
        self.fields["part_number"].choices = [(x[0], x[0]) for x in self.id_order_mas]


class ChangeOrderForm(forms.Form):
    conn.rollback()

    part_number = forms.ChoiceField(
        label="Выберите артикул из вашего заказа",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        cursor.execute(
            f"SELECT part_number FROM ordered_parts WHERE order_id={self.pk}"
        )
        self.id_order_mas = cursor.fetchall()
        self.fields["part_number"].choices = [(x[0], x[0]) for x in self.id_order_mas]


class AddPartForm(forms.Form):
    conn.rollback()

    part_number = forms.CharField(
        label="Артикул",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "single-input"})
    )

    part_name = forms.CharField(
        label="Название запчасти",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "single-input"})
    )

    manufacturer = forms.CharField(
        label="Производитель",
        max_length=255,
        required=False,  # Поле не обязательно
        widget=forms.TextInput(attrs={"class": "single-input"})
    )

    supplier = forms.CharField(
        label="Поставщик",
        max_length=255,
        required=False,  # Поле не обязательно
        widget=forms.TextInput(attrs={"class": "single-input"})
    )

    quantity_in_stock = forms.IntegerField(
        label="Количество на складе",
        min_value=0,  # Не допускает отрицательные значения
        widget=forms.NumberInput(attrs={"class": "single-input"})
    )

    price = forms.DecimalField(
        label="Цена",
        min_value=0.1,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "single-input"})
    )


class DelPartForm(forms.Form):
    conn.rollback()
    query1 = """
    SELECT part_number FROM parts;
    """
    cursor.execute(query1)
    id_parts_mas = cursor.fetchall()
    part_number = forms.ChoiceField(
        label="Артикул запчасти",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_race
        self.fields["part_number"].choices = [(x[0], x[0]) for x in self.id_parts_mas]


class ChangePartForm(AddPartForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        cursor.execute("SELECT * from get_parts_by_part_number(%s);", (self.pk,))
        self.def_value = cursor.fetchall()
        print(self.def_value)
        self.initial["part_name"] = self.def_value[0][0]
        self.initial["manufacturer"] = self.def_value[0][1]
        self.initial["supplier"] = self.def_value[0][2]
        self.initial["quantity_in_stock"] = self.def_value[0][3]
        self.initial["price"] = self.def_value[0][4]

