from flask import Flask, render_template, request
import sqlite3
import subprocess
import sys

app = Flask(__name__)

# Путь к базе данных SQLite
DB_FILE = "products.db"


# Функция для создания таблицы в базе данных
def create_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Создаем таблицу для продуктов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            price TEXT NOT NULL,
            image TEXT,
            year TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Функция для загрузки данных из базы данных
def load_products():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, link, price, image, year FROM products")
    rows = cursor.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = {
            "name": row[0],
            "link": row[1],
            "price": row[2],
            "image": row[3],
            "year": row[4],
        }
        products.append(product)
    return products


# Функция сортировки
def sort_products(products, sort_by_price_desc=False, sort_by_price_asc=False, sort_alphabetically=False):
    if sort_alphabetically:
        return sorted(products, key=lambda x: x['name'].lower())
    if sort_by_price_desc:
        return sorted(products, key=lambda x: -(float(x['price']) if x['price'] != "Нет в наличии" else 0))
    if sort_by_price_asc:
        return sorted(products, key=lambda x: (float(x['price']) if x['price'] != "Нет в наличии" else 0))
    return products





@app.route("/", methods=["GET", "POST"])
def index():

    sort_by = request.args.get("sort", "price_desc")  # Получаем текущий способ сортировки
    filter_year = request.args.get("year", "all")  # Получаем текущий фильтр по году
    page = int(request.args.get("page", 1))  # Номер текущей страницы

    # Загружаем данные
    products = load_products()

    # Фильтрация по году
    if filter_year != "all":
        products = [p for p in products if p['year'] == filter_year]

    # Сортировка продуктов
    if sort_by == "price_desc":
        products = sort_products(products, sort_by_price_desc=True)
    elif sort_by == "price_asc":
        products = sort_products(products, sort_by_price_asc=True)
    elif sort_by == "alphabetical":
        products = sort_products(products, sort_alphabetically=True)

    # Пагинация
    items_per_page = 28
    total_pages = len(products) // items_per_page + (1 if len(products) % items_per_page > 0 else 0)

    # Проверка на допустимый номер страницы
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_index = (page - 1) * items_per_page
    end_index = page * items_per_page
    products_on_page = products[start_index:end_index]

    # Генерация списка страниц для отображения
    if total_pages <= 3:
        display_pages = list(range(1, total_pages + 1))
    else:
        if page == 1:
            display_pages = [1, 2, 3]
        elif page == total_pages:
            display_pages = [total_pages - 2, total_pages - 1, total_pages]
        else:
            display_pages = [page - 1, page, page + 1]

    # Уникальные годы для фильтрации
    unique_years = sorted({p['year'] for p in products if p['year'] != "Не указан"})

    return render_template(
        "index.html",
        products=products_on_page,
        sort_by=sort_by,
        filter_year=filter_year,
        page=page,
        display_pages=display_pages,
        unique_years=unique_years,
        total_pages=total_pages
    )


if __name__ == "__main__":
    create_db()
    app.run(debug=True)

