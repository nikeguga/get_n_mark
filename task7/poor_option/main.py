import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URL для скрейпинга
url = 'http://books.toscrape.com/catalogue/page-{}.html'

# Настройка Selenium с использованием Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Для работы без графического интерфейса
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Функция для получения данных с одной страницы
def scrape_page(driver, page_number):
    driver.get(url.format(page_number))
    time.sleep(2)  # Небольшая задержка для полной загрузки страницы
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    books_data = []
    
    # Поиск всех элементов с книгами
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        # Извлечение названия книги
        title = book.h3.a['title']

        # Извлечение цены
        price = book.find('p', class_='price_color').text[1:]  # Убираем символ валюты

        # Извлечение рейтинга
        rating_class = book.p['class'][1]
        rating = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }.get(rating_class, 'No rating')

        # Извлечение доступности
        availability = book.find('p', class_='instock availability').text.strip()

        books_data.append([title, price, rating, availability])

    return books_data

# Главная функция для управления процессом скрейпинга
def main():
    driver = setup_driver()
    all_books_data = []

    # Собираем данные с первых 3 страниц
    for page in range(1, 4):
        print(f"Скрейпинг страницы {page}...")
        try:
            books_data = scrape_page(driver, page)
            all_books_data.extend(books_data)
        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")

    driver.quit()

    # Сохраняем данные в CSV
    with open('C:\\Users\\User\\Desktop\\Get_n_mark_data\\task7\\poor_option\\output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price (£)', 'Rating', 'Availability'])
        writer.writerows(all_books_data)
    
    print("Данные успешно сохранены в output.csv")

if __name__ == '__main__':
    main()
