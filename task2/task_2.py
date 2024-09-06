import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = "http://books.toscrape.com/"
CATEGORY_URL = "http://books.toscrape.com/catalogue/category/books_1/index.html"

# Получение всех категорий
def get_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find('ul', class_='nav-list').find('ul').find_all('a')
    category_urls = [BASE_URL + category['href'] for category in categories]
    return category_urls

# Извлечение информации о книге с ее страницы
def get_book_info(book_url):
    # Получение страницы книги
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Получение данных о книге (пример)
    title = soup.find('h1').text
    price = soup.find('p', class_='price_color').text  # Пример: '£45.17'

    # Удаление символов валюты и пробелов из строки
    price = price.replace('Â', '').strip()  # Убираем символы, мешающие преобразованию
    price = price.replace('£', '')  # Убираем символ фунта

    # Преобразование строки в float
    try:
        price = float(price)
    except ValueError as e:
        print(f"Ошибка преобразования цены: {price}, {e}")
        price = None  # Можем установить значение None, если цена не распознается

    # Пример получения описания и количества книг в наличии
    stock = soup.find('p', class_='instock availability').text.strip()
    in_stock = int(stock.split('(')[1].split(' ')[0])  # Пример: 'In stock (19 available)' -> 19
    
    description = soup.find('meta', {'name': 'description'})['content'].strip() if soup.find('meta', {'name': 'description'}) else "Описание недоступно"

    # Возвращаем данные о книге в виде словаря
    return {
        'title': title,
        'price': price,
        'in_stock': in_stock,
        'description': description
    }


# Извлечение информации о книгах с одной страницы категории
def get_books_from_page(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    book_data = []
    for book in books:
        book_url = BASE_URL + 'catalogue/' + book.find('h3').find('a')['href'].replace('../../../', '')
        book_info = get_book_info(book_url)
        book_data.append(book_info)
    
    return book_data

# Пагинация: извлечение данных с каждой страницы категории
def scrape_category(category_url):
    category_data = []
    while True:
        category_data.extend(get_books_from_page(category_url))
        
        # Проверяем, есть ли ссылка на следующую страницу
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_button = soup.find('li', class_='next')
        
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_page_url
        else:
            break
    
    return category_data

# Основная функция для скрейпинга всех категорий и книг
def scrape_all_books():
    categories = get_categories()
    all_books_data = []
    
    for category_url in categories:
        print(f'Scraping category: {category_url}')
        category_books = scrape_category(category_url)
        all_books_data.extend(category_books)
    
    return all_books_data

# Сохранение данных в JSON
def save_to_json(data, filename="books_data.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Запуск процесса скрейпинга
if __name__ == "__main__":
    all_books = scrape_all_books()
    save_to_json(all_books)
    print(f"Scraped {len(all_books)} books and saved to books_data.json")
