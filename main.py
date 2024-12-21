from flask import Flask, render_template_string
import pandas as pd
import sqlite3


data = {
  'Имя': ['Анна', 'Мария', 'Иван', 'Егор', 'Николай', 'Алина', 'Ольга', 'Михаил', 'Григорий', 'Василий'],
  'Подарок': ['Ваза', 'Сертификат', 'Часы', 'Шоколад', 'Косметика', 'Крем', 'Чай', 'Телефон', 'Сертификат',
              'Сертификат'],
  'Стоимость': [500, 1000, 10000, 200, 600, 100, 700, 12000, 1500, 1000],
  'Статус': ['Куплено', 'Заказано', 'Заказано', 'Забрать заказ', 'Забрать заказ', 'В пути', 'Не куплено', 'Не куплено',
             'Не куплено', 'Куплено']
}

wish_list = pd.DataFrame(data)
print(wish_list)

connection = sqlite3.connect('wish_list.db')

wish_list.to_sql('wish_list', connection, index=False, if_exists='replace')

sql = ''' select *
            from wish_list

'''
# Проверка наличия данных в вашей таблице написав SQL запрос через Python
pd.read_sql(sql, connection)

html_template = """
    <!doctype html>
    <html>
        <head>
            <title>Список подарков</title>
        </head>
        <body>
            <h1>Список подарков</h1>
            <table border="1">
                <tr>
                    <th>Имя</th>
                    <th>Подарок</th>
                    <th>Стоимость</th>
                    <th>Статус</th>
                </tr>
                {% for gift in gifts %}
                <tr>
                    <td>{{ gift[0] }}</td>
                    <td>{{ gift[1] }}</td>
                    <td>{{ gift[2] }}</td>
                    <td>{{ gift[3] }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """


app = Flask(__name__)

@app.route('/')
def index():
    # Подключаемся к базе данных
    conn = sqlite3.connect('wish_list.db')
    cursor = conn.cursor()

    # Извлекаем данные из таблицы
    cursor.execute('SELECT * FROM wish_list')
    wish_list = cursor.fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    return render_template_string(html_template, gifts=wish_list)

if __name__ == '__main__':
    app.run(debug=True)

