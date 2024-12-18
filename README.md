# Магазин Велосипедов

Проект представляет собой веб-приложение для парсинга и отображения данных о горных велосипедах с возможностью сортировки, фильтрации и пагинации. Приложение разработано с использованием Python, Flask и SQLite.

## Основные функции

- **Парсинг данных**: Автоматический сбор данных о горных велосипедах с сайта [velostrana.ru](https://www.velostrana.ru).
- **База данных**: Сохранение данных в локальной базе данных SQLite.
- **Веб-интерфейс**: Отображение данных на веб-странице с возможностью:
  - сортировки (по цене и алфавиту);
  - фильтрации по году;
  - пагинации.
- **Docker**: Поддержка контейнеризации для удобного развёртывания.

---

## Технологии

- **Язык программирования**: Python 3.8
- **Библиотеки**:
  - `Flask` для разработки веб-интерфейса;
  - `BeautifulSoup` для парсинга HTML;
  - `sqlite3` для работы с базой данных;
  - `requests` для работы с HTTP-запросами.
- **База данных**: SQLite
- **Шаблоны HTML**: Jinja2
- **Docker**: Для развёртывания приложения в контейнерах.

---

## Установка и запуск

### Предварительные требования

- Установленный Docker и Docker Compose.
- Установленный Python 3.8 (для запуска без Docker).

### Запуск с помощью Docker

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/ZeroR0cks/velo1.git
   cd velo1/velosport
   ```

2. Запустите приложение:

   ```bash
   ./build.sh
   ```

3. Приложение будет доступно по адресу: `http://localhost:5000`


---

## Использование

### Веб-интерфейс

- **Сортировка**:
  - По убыванию цены.
  - По возрастанию цены.
  - По алфавиту.
- **Фильтрация**:
  - Выбор года выпуска велосипеда.
  - Просмотр всех доступных годов.
- **Пагинация**:
  - Переход между страницами товаров.

---

## Архитектура

### Основные модули

1. **Парсер (`parser.py`)**:

   - Скачивает HTML-код страниц.
   - Извлекает информацию о велосипедах (название, цена, ссылка, изображение, год).
   - Сохраняет данные в SQLite.

2. **База данных (`products.db`)**:

   - Таблица `products` для хранения информации о товарах.
   - Поля: `id`, `name`, `link`, `price`, `image`, `year`.

3. **Веб-приложение (Flask)**:

   - Загружает данные из базы данных.
   - Реализует фильтрацию, сортировку и пагинацию.
   - Отображает данные на HTML-странице с использованием шаблонов Jinja2.

4. **Docker**:

   - Файлы: `Dockerfile`, `docker-compose.yml` для удобной контейнеризации.

---

## Структура проекта

```
.
├── velosport/          # Основная папка проекта
│   ├── app.py          # Основной файл Flask-приложения
│   ├── parser.py       # Логика парсинга данных
│   ├── products.db     # SQLite база данных
│   ├── requirements.txt # Список зависимостей проекта
│   ├── Dockerfile      # Конфигурация для сборки Docker-образа
│   └── templates/      # HTML-шаблоны
│       └── index.html  # Основная страница
│   
├── README.md           # Документация проекта
├── docker-compose.yml # Конфигурация Docker Compose
└── build.sh          # Скрипт для запуска приложения

```


