import scrapy
from random import choice
from book_scraper.settings import USER_AGENTS  # Импортируем список User-Agent'ов

class LabirintSpider(scrapy.Spider):
    name = "labirint_spider"
    allowed_domains = ["labirint.ru"]

    # Стартовый URL с поиском по ключевому слову "научная фантастика"
    start_urls = [
        'https://www.labirint.ru/search/%D0%BD%D0%B0%D1%83%D1%87%D0%BD%D0%B0%D1%8F%20%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0'
    ]

    def start_requests(self):
        headers = {
            'User-Agent': choice(USER_AGENTS)
        }
        for url in self.start_urls:
            self.log(f"Отправляем запрос на URL: {url}")
            yield scrapy.Request(url=url, headers=headers)

    def parse(self, response):
        self.log(f"Получен ответ на URL: {response.url} со статусом {response.status}")

        # Проверка содержимого страницы
        if response.status == 200:
            self.log(f"Содержимое страницы (первые 500 символов): {response.text[:500]}")

        # Извлечение списка книг на текущей странице
        books = response.css('a.product-card__name::attr(href)').getall()  # Извлечение ссылок на книги
        self.log(f"Найдено {len(books)} книг на странице.")

        if not books:
            self.log("Не удалось найти книги на странице.")

        for book in books:
            book_url = response.urljoin(book)
            headers = {
                'User-Agent': choice(USER_AGENTS)
            }
            # Переходим на страницу каждой книги
            self.log(f"Переход к книге: {book_url}")
            yield scrapy.Request(url=book_url, callback=self.parse_book_details, headers=headers)

        # Переход на следующую страницу, если есть
        next_page = response.css('a.pagination-next__text::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            headers = {
                'User-Agent': choice(USER_AGENTS)
            }
            self.log(f"Переход на следующую страницу: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse, headers=headers)

    def parse_book_details(self, response):
        # Извлечение данных о книге
        title = response.css('h1::text').get()
        author = response.css('div.authors a::text').get()
        book_id = response.css('div.articul::text').get().strip().replace("ID товара: ", "")
        isbn = response.css('div.isbn::text').get().strip().replace("ISBN: ", "")
    
        # Новый селектор для аннотации
        annotation = response.css('div#product-about p::text').getall()
        annotation = ' '.join(annotation).strip()

        # Логирование для отладки
        self.log(f"Книга: {title}, Автор: {author}, ID: {book_id}, ISBN: {isbn}, Аннотация: {annotation}")

        # Вывод данных в файл
        yield {
            'title': title,
            'author': author,
            'id': book_id,
            'isbn': isbn,
            'annotation': annotation,
        }


