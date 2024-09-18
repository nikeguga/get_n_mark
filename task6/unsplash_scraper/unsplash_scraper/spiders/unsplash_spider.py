import scrapy
import os
import csv
from ..items import UnsplashImageItem

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash_spider'

    query = "space"
    start_urls = [f"https://unsplash.com/s/photos/{query}?license=free"]

    def __init__(self):
        super().__init__()
        # Открываем CSV-файл для записи
        self.csv_file = open('output.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        # Записываем заголовки
        self.csv_writer.writerow(['Image URL', 'Local Path', 'Title', 'Categories'])

    def parse(self, response):
        # Находим все ссылки на страницы изображений
        image_links = response.css('a[href*="/photos/"]::attr(href)').getall()

        for link in image_links:
            # Извлекаем категории на странице результата поиска
            categories = response.css('a[data-test="photo-tags-link"]::text').getall()

            # Пропускаем, если нет категорий
            if not categories:
                continue

            # Переходим на страницу изображения
            yield response.follow(link, callback=self.parse_image, meta={'categories': categories})

    def parse_image(self, response):
        # Извлекаем все элементы img с srcset, чтобы найти нужное изображение
        images = response.css('img[srcset]')

        # Пропускаем первый srcset, как он относится к изображению профиля
        if len(images) > 1:
            # Второй srcset содержит изображение картины
            image = images[1]
            image_src = image.css('::attr(srcset)').get()

            if image_src:
                # В srcset может быть несколько ссылок на разные разрешения, выбираем первое (с наименьшим разрешением)
                image_url = image_src.split(",")[0].split(" ")[0]

                # Извлекаем значение атрибута alt для использования в качестве имени изображения
                alt_text = image.css('::attr(alt)').get() or "image"

                # Формируем локальный путь к файлу после загрузки
                local_path = os.path.join('images', f"{alt_text}.jpg")

                # Записываем данные в CSV
                categories = response.meta['categories']
                self.csv_writer.writerow([image_url, local_path, alt_text, ', '.join(categories)])

                # Возвращаем данные
                yield {
                    'title': alt_text,  # Используем alt как название файла
                    'image_urls': [image_url],
                }
            else:
                self.logger.info(f"No image src found on page: {response.url}")
        else:
            self.logger.info(f"Not enough images found on page: {response.url}")

    def closed(self, reason):
        # Закрываем CSV-файл при завершении работы паука
        self.csv_file.close()
