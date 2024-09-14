import requests
from lxml import html
import csv
import time

# URL страницы для парсинга
url = 'https://news.mail.ru/'

# Заголовок User-Agent, чтобы имитировать работу браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Функция для парсинга содержимого статьи по ссылке
def parse_article(link):
    try:
        article_response = requests.get(link, headers=headers)
        if article_response.status_code == 200:
            article_tree = html.fromstring(article_response.content)
            # Используем новый XPath для получения всех параграфов текста статьи
            paragraphs = article_tree.xpath('//div[@data-qa="Text"]//p/text()')
            article_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
            return article_content if article_content else "No content"
        else:
            return "No content"
    except Exception as e:
        return f"Error: {e}"

try:
    # Отправка HTTP GET-запроса для главной страницы
    response = requests.get(url, headers=headers)

    # Проверяем статус ответа
    if response.status_code == 200:
        # Парсинг HTML содержимого с помощью lxml
        tree = html.fromstring(response.content)

        # Извлекаем все новости, которые представлены как блоки с изображением
        news_with_image = tree.xpath('//a[contains(@class, "newsitem") and .//img]')
        # Извлекаем все текстовые новости
        text_news = tree.xpath('//a[contains(@class, "newsitem") and not(.//img)]')

        # Путь для сохранения CSV файла
        csv_file_path = r'C:\Users\User\Desktop\Get_n_mark_data\task4\news_mail_ru.csv'

        # Открываем файл для записи
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Link', 'Article Content'])

            # Парсинг новостей с изображениями
            for news in news_with_image:
                title = news.xpath('.//span/text()')
                title = title[0] if title else "No title"
                link = news.xpath('./@href')
                link = link[0] if link else "No link"

                # Парсим содержимое статьи по ссылке
                article_content = parse_article(link)
                
                writer.writerow([title, link, article_content])
                time.sleep(1)  # Задержка между запросами, чтобы не перегружать сервер

            # Парсинг текстовых новостей
            for news in text_news:
                title = news.xpath('.//span/text()')
                title = title[0] if title else "No title"
                link = news.xpath('./@href')
                link = link[0] if link else "No link"

                # Парсим содержимое статьи по ссылке
                article_content = parse_article(link)
                
                writer.writerow([title, link, article_content])
                time.sleep(1)  # Задержка между запросами, чтобы не перегружать сервер

        print(f"Данные успешно сохранены в файл {csv_file_path}")

    else:
        print(f"Не удалось получить данные. Статус ответа: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP запроса: {e}")

except Exception as e:
    print(f"Произошла ошибка: {e}")
