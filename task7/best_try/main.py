import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Настройка Selenium с использованием Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в headless режиме
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Функция для выполнения поиска и установки фильтров
def search_and_filter(driver):
    # Переход на главную страницу eBay
    driver.get('https://www.ebay.com/')
    time.sleep(4)

    # Поиск по ключевому слову "guitar"
    search_box = driver.find_element(By.NAME, '_nkw')
    search_box.send_keys('guitar')
    search_box.send_keys(Keys.RETURN)
    time.sleep(4)

    # Применение фильтра по состоянию (Used)
    try:
        used_filter = driver.find_element(By.XPATH, '//input[@aria-label="Used"]')
        used_filter.click()
        time.sleep(4)
    except NoSuchElementException:
        print("Фильтр по б/у товарам не найден.")

# Функция для извлечения данных с каждой страницы товара
def scrape_item_page(driver, item_url):
    driver.get(item_url)
    time.sleep(4)  # Даем странице загрузиться
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        # Извлечение заголовка
        title = soup.find('h1', class_='x-item-title__mainTitle').text.strip()
    except:
        title = "No title"
    
    return title

# Функция для извлечения ссылок и других данных со страницы поиска
def scrape_search_results(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('li', class_='s-item')

    item_data = []
    for item in items:
        try:
            # Ссылка на товар
            link = item.find('a', class_='s-item__link')['href']
            
            # Цена товара
            price = item.find('span', class_='s-item__price').text.strip() if item.find('span', class_='s-item__price') else 'No price'

            # Количество предложений/просмотров
            status = item.find('span', class_='s-item__bids').text.strip() if item.find('span', class_='s-item__bids') else 'No bids/views'
            
            item_data.append([price, status, link])
        except:
            continue
    return item_data

# Переход на следующую страницу с использованием ссылки
# Функция для перехода на следующую страницу с возвратом к сохранённому URL
def go_to_next_page(driver, search_results_url):
    try:
        # Возвращаемся на сохранённый URL страницы результатов поиска
        driver.get(search_results_url)
        time.sleep(5)  # Увеличенная задержка для полной загрузки страницы

        # Ищем элемент кнопки "Next" и извлекаем URL
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagination__next.icon-link'))
        )
        next_page_url = next_button.get_attribute('href')

        if next_page_url:
            print(f"Переходим на следующую страницу: {next_page_url}")
            driver.get(next_page_url)  # Переходим по ссылке на следующую страницу
            time.sleep(5)  # Задержка для полной загрузки следующей страницы
        else:
            print("Ссылка на следующую страницу не найдена, завершаем сбор данных.")
            return False
    except NoSuchElementException:
        print("Кнопка 'Next' не найдена, завершаем сбор данных.")
        return False
    return True




# Главная функция для управления процессом скрейпинга
def main():
    driver = setup_driver()

    # Выполняем поиск и применяем фильтры
    search_and_filter(driver)

    all_items_data = []
    page = 1

    # Сохраняем текущий URL страницы результатов поиска после применения фильтров
    search_results_url = driver.current_url

    while len(all_items_data) < 100:  # Лимит в 100 товаров
        print(f"Скрейпинг страницы {page}...")

        try:
            # Получаем данные (цены, просмотры, ссылки) со страницы поиска
            items_data = scrape_search_results(driver)

            # Для каждого товара переходим на его страницу для получения заголовка
            for item in items_data:
                if len(all_items_data) >= 100:  # Лимит в 100 товаров
                    break
                price, status, item_url = item
                try:
                    title = scrape_item_page(driver, item_url)  # Переход на страницу товара для извлечения заголовка

                    # Убираем некорректные записи, такие как "No title" и "No price"
                    if title != "No title" and price != "No price":
                        all_items_data.append([title, price, status, item_url])
                except Exception as e:
                    print(f"Ошибка при переходе на страницу товара: {e}")

            # Переход на следующую страницу результатов поиска
            if not go_to_next_page(driver, search_results_url):
                break

            # После перехода на следующую страницу обновляем URL страницы результатов
            search_results_url = driver.current_url

        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
            break

        page += 1

    driver.quit()

    # Ограничиваем данные до 100 элементов
    all_items_data = all_items_data[:100]

    # Сохраняем данные в CSV
    with open('C:\\Users\\User\\Desktop\\Get_n_mark_data\\task7\\best_try\\output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Bids/Views', 'Link'])
        writer.writerows(all_items_data)

    print("Данные успешно сохранены в output.csv")

if __name__ == '__main__':
    main()
