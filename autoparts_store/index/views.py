from django.shortcuts import redirect, render, get_object_or_404
from globals import cursor, conn


# from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    conn.rollback()
    # View code here...
    user = request.user
    query1 = """ 
    SELECT *
    FROM Parts;
    """
    cursor.execute(query1)
    full = cursor.fetchall()  # для каталога

    cursor.execute(f"SELECT * FROM count_user_orders1({user.id})")
    count_orders = cursor.fetchone()[0]

    names_mas = []
    for x in range(len(full)):
        names_mas.append(
            {
                "id": full[x][0],
                "name": full[x][1],
                "man": full[x][2],
                "sup": full[x][3],
                "price": full[x][5],
            }
        )
    is_superuser = request.user.is_superuser
    context = {
        "parts": names_mas,
        "is_superuser": is_superuser,
        "count_orders": count_orders,
    }
    conn.rollback()
    return render(request, "index/main.html", context)


def my_orders(request):
    user = request.user
    # cursor.execute(f"SELECT * FROM user_orders_details1 WHERE order_id IN (SELECT order_id FROM Orders WHERE client_id = {user.id});")
    cursor.execute(
        f"SELECT order_id,sum(unit_price),order_date FROM user_orders_details1 WHERE order_id IN (SELECT order_id FROM Orders WHERE client_id = {user.id}) GROUP BY order_id,order_date;"
    )
    data = cursor.fetchall()
    names_mas = []
    for x in range(len(data)):
        names_mas.append(
            {"id_order": data[x][0], "total_sum": data[x][1], "order_date": data[x][2]}
        )

    context = {
        "orders": names_mas,
    }
    conn.rollback()
    return render(request, "index/my_orders.html", context)


def order_detail(request, pk):
    cursor.execute(f"SELECT * FROM user_orders_details1 WHERE order_id = {pk};")
    data = cursor.fetchall()
    names_mas = []
    for x in range(len(data)):
        names_mas.append(
            {
                "id_order": data[x][0],
                "order_date": data[x][1],
                "total_sum": data[x][2],
                "part_number": data[x][3],
                "part_name": data[x][4],
                "manufacturer": data[x][5],
                "sup": data[x][6],
                "unit_price": data[x][7],
                "quantity": data[x][8],
                "price": data[x][9]
            }
        )
    context = {
        "orders": names_mas,
    }
    conn.rollback()
    return render(request, "index/order_detail.html", context)
