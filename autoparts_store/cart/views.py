from django.shortcuts import redirect, render, get_object_or_404
from globals import cursor, conn
from .forms import ProductQuantityForm
from .models import Cart, CartItem


# Create your views here.
def add_cart(request, art):  # добавление в корзину
    cursor.execute("SELECT * FROM get_part_details(%s);", (art,))
    data = cursor.fetchall()
    quantity = data[0][3]  # кол-во на складе
    price = data[0][4]
    name = data[0][0]
    if request.method == "POST":
        form = ProductQuantityForm(request.POST, count_max=quantity)

        if form.is_valid():
            """Добавить продукт в корзину."""
            # Получение или создание корзины пользователя
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Проверка, есть ли уже этот продукт в корзине
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                part_number=art,
                price=price,
            )

            if not created:
                # Если продукт уже в корзине, просто увеличиваем количество
                if cart_item.quantity + form.cleaned_data["quantity"] > quantity:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += form.cleaned_data["quantity"]
            else:
                cart_item.quantity = form.cleaned_data["quantity"]

            # Обновление цены на случай, если она изменилась или устанавливаем первоначальную цену
            cart_item.save()  # Сохраняем изменения (добавление или обновление

            return redirect("index")  # Перенаправление на страницу

            return redirect(
                "index",
            )  # Перенаправляем на страницу успеха или другую страницу

    else:
        form = ProductQuantityForm(count_max=quantity)

    conn.rollback()
    return render(
        request,
        "cart/add_cart.html",
        {
            "form": form,
            "our_url": "add_cart",
            "art": art,
            "price": price,
            "name": name,
            "count": quantity,
            "title": "Добавление товара в корзину",
            "button_title": "Добавить в корзину",
        },
    )


def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()  # Получаем все элементы в корзине
        total = sum(item.total_price for item in cart_items)  # Общая сумма
    except Cart.DoesNotExist:
        cart_items = []  # Если корзина не существует, создаем пустой список
        total = 0
    print(cart_items)
    a = []
    for i in cart_items:
        cursor.execute("SELECT part_name FROM get_part_details(%s);", (i.part_number,))
        data = cursor.fetchone()
        a.append(
            {
                "id": i.id,
                "part_number": i.part_number,
                "name": data[0],
                "quantity": i.quantity,
                "price": i.price,
                "total_price": i.total_price,
            }
        )
    conn.rollback()
    return render(
        request,
        "cart/view_cart.html",
        {"cart_items": cart_items, "cart": cart, "total": total, "a": a},
    )


def remove_from_cart(request, item_id):
    # Находим элемент корзины по его ID
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Удаляем элемент из корзины
    cart_item.delete()

    # Перенаправляем пользователя на страницу корзины
    return redirect("view_cart")


def add_order(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()  # Получаем все элементы в корзине
        total = sum(item.total_price for item in cart_items)  # Общая сумма
    except Cart.DoesNotExist:
        cart_items = []  # Если корзина не существует, создаем пустой список
        total = 0
    user = request.user
    a = []
    for i in cart_items:
        cursor.execute("SELECT part_name FROM get_part_details(%s);", (i.part_number,))
        data = cursor.fetchone()
        a.append(
            {
                "id": i.id,
                "part_number": i.part_number,
                "name": data[0],
                "quantity": i.quantity,
                "price": i.price,
                "total_price": i.total_price,
            }
        )
    print(total)
    if total != 0:
        cursor.execute("SELECT insert_order(%s, %s);", (user.id, total))
        id_order = data = cursor.fetchone()[0]
        conn.commit()
        print(id_order)
        print(a)
        for elem in a:
            cursor.execute(
                "SELECT insert_ordered_part(%s,%s,%s, %s);",
                (id_order, elem["part_number"], elem["quantity"], elem["total_price"]),
            )
            conn.commit()
        cart.clear_cart()  # очищаем корзину после заказа
    conn.rollback()
    return render(
        request,
        "cart/happy_add.html"
    )
