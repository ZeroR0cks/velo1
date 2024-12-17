import requests
from bs4 import BeautifulSoup
import re
import sqlite3

# Имя файла базы данных
DB_FILE = "products.db"

# Подключение к БД и создание таблицы
def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
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

# Вставка данных в БД
def write_to_db(products: list[Product]):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for product in products:
        cursor.execute('''
            INSERT INTO products (name, link, price, image, year) 
            VALUES (?, ?, ?, ?, ?)
        ''', (product.name, product.link, product.price, product.image, product.year))
    conn.commit()
    conn.close()

# Извлечение года из названия
def extract_year_from_name(name: str) -> str:
    match = re.search(r"\((\d{4})\)$", name)
    return match.group(1) if match else "Не указан"

# Основной парсер
def parser(url: str, total_items: int = 3428):
    initialize_db()  # Создание БД и таблицы
    page = 1
    count_items = 0

    while count_items < total_items:
        list_product = []
        res = requests.get(f"{url}{page}.html")
        soup = BeautifulSoup(res.text, "lxml")
        products = soup.find_all("div", class_="product-card")

        if not products:
            break

        for product in products:
            velo = product.find("div", class_="product-card__category")
            if velo and "горный велосипед" in velo.get_text(strip=True).lower():
                name = product.find("div", class_="product-card__model")
                if name:
                    name_text = name.get_text(strip=True)
                    year = extract_year_from_name(name_text)
                    price_tag = product.find("meta", itemprop="lowPrice")
                    price = price_tag.get("content") if price_tag and price_tag.get("content") != "0" else "Нет в наличии"
                    link_tag = product.find("a", class_="product-card__title")
                    link = f"https://www.velostrana.ru{link_tag.get('href')}" if link_tag else "Ссылка не найдена"
                    image_tag = product.find("img", itemprop="image")
                    image_url = image_tag.get("src") if image_tag and image_tag.get("src") != "/assets/images/server_s_foto.svg" else "https://fitowatt.ru/assets/static/noimage.jpg"

                    list_product.append(Product(name=name_text, link=link, price=price, image=image_url, year=year))
                    count_items += 1
                    print(f"Обработан товар {count_items}: {name_text}, Цена: {price}, Год: {year}")

                    if count_items >= total_items:
                        break

        write_to_db(list_product)  # Запись в БД
        page += 1

if __name__ == "__main__":
    parser(url="https://www.velostrana.ru/gornye-velosipedy/")
