import psycopg2
try:
    conn = psycopg2.connect(
            dbname="masha",
            user="postgres",
            password="123",
            host="127.0.0.1",
            port="5433",
        )
except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
    print("<h1>Потеряно подключение к базе данных!</h1>")

cursor = conn.cursor()