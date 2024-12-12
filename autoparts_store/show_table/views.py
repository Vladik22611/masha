from django.shortcuts import render
from globals import cursor, conn


def table(request, name_table):
    query1 = f"""SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{name_table}';
    """

    cursor.execute(query1)
    column_name = cursor.fetchall()
    mas_column_name = []
    for i in column_name:
        mas_column_name.append(i[0])

    query2 = f"""SELECT * 
            FROM {name_table};
    """
    cursor.execute(query2)
    data = cursor.fetchall()

    return render(
        request,
        "show_table/show_table.html",
        {"title": f"Таблица {name_table}", "columns": mas_column_name, "data": data},
    )


# Create your views here.
