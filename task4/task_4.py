import requests
from lxml import html
import csv
import os

# URL страницы с таблицей
url = 'https://ninjatables.com/examples-of-data-table-design-on-website/'

# Заголовок User-Agent, чтобы имитировать работу браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # Отправка HTTP GET-запроса
    response = requests.get(url, headers=headers)

    # Проверяем статус ответа
    if response.status_code == 200:
        # Парсинг HTML содержимого с помощью lxml
        tree = html.fromstring(response.content)

        # XPath выражение для извлечения строк таблицы
        rows = tree.xpath('//*[@id="footable_17874"]//tr')

        # Путь для сохранения CSV файла
        csv_file_path = os.path.join('C:\\Users\\User\\Desktop\\Get_n_mark_data\\task4', 'extracted_data.csv')

        # Открываем файл для записи
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Обрабатываем строки таблицы
            for row in rows:
                # Извлекаем текст из каждой ячейки
                cells = row.xpath('.//td/text() | .//th/text()')
                
                # Если есть данные в строке, записываем их в CSV
                if cells:
                    writer.writerow([cell.strip() for cell in cells])

        print(f"Данные успешно сохранены в файл {csv_file_path}")

    else:
        print(f"Не удалось получить данные. Статус ответа: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP запроса: {e}")

