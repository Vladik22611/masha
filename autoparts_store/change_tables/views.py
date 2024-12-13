from django.shortcuts import redirect, render
from .forms import (
    AddPartForm,
    ChangePartForm,
    ChoicePartNumberForm,
    DelOrderForm,
    DelPartForm,
)
from globals import conn, cursor
from cart.forms import ProductQuantityForm


def del_order(request):
    if request.method == "POST":
        form = DelOrderForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            cursor.execute(
                "SELECT delete_order(%s)",
                (form.cleaned_data["id_order"],),
            )
            conn.commit()
            return render(
                request,
                "change_tables/happy_change.html",
                {
                    "title": "Удаление заказа",
                },
            )  # Перенаправляем на страницу успеха или другую страницу

    else:
        form = DelOrderForm()

    conn.rollback()
    return render(
        request,
        "change_tables/change.html",
        {
            "form": form,
            "our_url": "del_order",
            "title": "Удаление заказа",
            "button_title": "Удалить заказ",
        },
    )


def change_order(request):
    if request.method == "POST":
        form = DelOrderForm(request.POST)
        if form.is_valid():
            return redirect(
                "change_order_def", pk=form.cleaned_data["id_order"]
            )  # Перенаправляем на страницу успеха или другую страницу
    else:
        form = DelOrderForm()

    return render(
        request,
        "change_tables/change.html",
        {
            "form": form,
            "our_url": "change_order",
            "title": "Изменение заказа",
            "button_title": "Изменить заказ",
        },
    )


def change_order_def(request, pk):
    if request.method == "POST":
        form = ChoicePartNumberForm(request.POST, pk=pk)
        if form.is_valid():
            return redirect(
                "change_order_def_next",
                pk=pk,
                part_number=form.cleaned_data["part_number"],
            )  # Перенаправляем на страницу успеха или другую страницу
    else:
        form = ChoicePartNumberForm(pk=pk)

    return render(
        request,
        "change_tables/change_pk.html",
        {
            "form": form,
            "our_url": "change_order_def",
            "pk": pk,
            "title": "Изменение заказа",
            "button_title": "Выбрать",
        },
    )


def change_order_def_next(request, pk, part_number):
    cursor.execute(
        f"SELECT quantity_in_stock FROM parts WHERE part_number='{part_number}'"
    )
    max_count = cursor.fetchall()[0][0]

    cursor.execute(
        f"SELECT price FROM parts WHERE part_number='{part_number}'"
    )
    price = cursor.fetchall()[0][0]

    print(max_count)
    if request.method == "POST":
        form = ProductQuantityForm(request.POST, count_max=max_count)
        if form.is_valid():
            cursor.execute(
                "SELECT update_order(%s,%s,%s);",
                (pk, part_number, form.cleaned_data["quantity"]),
            )
            conn.commit()
            return render(
                request,
                "change_tables/happy_change.html",
                {
                    "title": "Изменение заказа",
                },
            )  # Перенаправляем на страницу успеха или другую страницу
    else:
        form = ProductQuantityForm(count_max=max_count)

    return render(
        request,
        "change_tables/change_pk_part.html",
        {
            "form": form,
            "our_url": "change_order_def_next",
            "pk": pk,
            "part_number": part_number,
            "count": max_count,
            "unit_price": price,
            "title": "Изменение заказа",
            "button_title": "Изменить",
        },
    )


def add_part(request):
    conn.rollback()
    if request.method == "POST":
        form = AddPartForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT insert_part(%s, %s, %s, %s, %s, %s)",
                    (
                        a["part_number"],
                        a["part_name"],
                        a["manufacturer"],
                        a["supplier"],
                        a["quantity_in_stock"],
                        a["price"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "change_tables/happy_change.html",
                    {
                        "title": "Добавление запчасти",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "повторяющееся значение ключа" in str(e):  # если триггер словил исключение
                    error_message = (
                        "Ошибка: артикул с такими же значениями уже существует!"
                    )
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                conn.rollback()
                return render(
                    request,
                    "change_tables/sad_change.html",
                    {
                        "title": error_message,
                    },
                )
            finally: pass 
    else:
        form = AddPartForm()
    
    return render(
        request,
        "change_tables/change.html",
        {
            "form": form,
            "our_url": "add_part",
            "title": "Добавление запчасти",
            "button_title": "Добавить",
        },
    )


def del_part(request):
    if request.method == "POST":
        form = DelPartForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            cursor.execute(
                "SELECT delete_part(%s)",
                (form.cleaned_data["part_number"],),
            )
            conn.commit()
            conn.rollback()
            return render(
                request,
                "change_tables/happy_change.html",
                {
                    "title": "Удаление запчасти",
                },
            )  # Перенаправляем на страницу успеха или другую страницу

    else:
        form = DelPartForm()
    conn.rollback()
    return render(
        request,
        "change_tables/change.html",
        {
            "form": form,
            "our_url": "del_part",
            "title": "Удаление запчасти",
            "button_title": "Удалить",
        },
    )


def change_part(request):
    if request.method == "POST":
        form = DelPartForm(request.POST)
        if form.is_valid():
            return redirect(
                "change_part_def", pk=form.cleaned_data["part_number"]
            )  # Перенаправляем на страницу успеха или другую страницу
    else:
        form = DelPartForm()

    return render(
        request,
        "change_tables/change.html",
        {
            "form": form,
            "our_url": "change_part",
            "title": "Изменение запчасти",
            "button_title": "Изменить",
        },
    )


def change_part_def(request, pk):
    conn.rollback()
    if request.method == "POST":
        form = ChangePartForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            print(a)
            try:
                cursor.execute(
                    "SELECT update_parts(%s,%s, %s, %s, %s, %s)",
                    (
                        pk,
                        a["part_name"],
                        a["manufacturer"],
                        a["supplier"],
                        a["quantity_in_stock"],
                        a["price"],
                    ),
                )
                conn.commit()
                conn.rollback()
                return render(
                    request,
                    "change_tables/happy_change.html",
                    {
                        "title": "Изменение запчасти",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException:
                error_message = "Произошла ошибка при изменении записи."
                return render(
                    request,
                    "change_tables/sad_change.html",
                    {
                        "title": error_message,
                    },
                )
    else:
        form = ChangePartForm(pk=pk)
    
    return render(
        request,
        "change_tables/change_part_pk.html",
        {
            "form": form,
            "our_url": "change_part_def",
            "pk": pk,
            "title": "Изменение запчасти",
            "button_title": "Изменить",
        },
    )


# Create your views here.
