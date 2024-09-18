import scrapy
from ..items import UnsplashImageItem

class UnsplashSpider(scrapy.Spider):
    name = 'unsplash_spider'

    query = "space"
    start_urls = [f"https://unsplash.com/s/photos/{query}?license=free"]

    def parse(self, response):
        # Находим все ссылки на страницы изображений
        image_links = response.css('a[href*="/photos/"]::attr(href)').getall()

        for link in image_links:
            # Переход на страницу изображения
            yield response.follow(link, callback=self.parse_image)

    def parse_image(self, response):
        # Извлекаем все элементы img с srcset, чтобы найти нужное изображение
        images = response.css('img[srcset]')

        # Пропускаем первый srcset, так как он относится к изображению профиля
        if len(images) > 1:
            # Второй srcset содержит изображение картины
            image = images[1]
            image_src = image.css('::attr(srcset)').get()

            if image_src:
                # В srcset может быть несколько ссылок на разные разрешения, выбираем первое (с наименьшим разрешением)
                image_url = image_src.split(",")[0].split(" ")[0]

                # Извлекаем значение атрибута alt для использования в качестве имени изображения
                alt_text = image.css('::attr(alt)').get() or "image"

                # Логирование для отладки
                self.logger.info(f"Found image: {image_url} with alt: {alt_text}")

                # Возвращаем данные
                yield UnsplashImageItem(
                    title=alt_text,        # Используем alt как название файла
                    image_urls=[image_url], # URL изображения
                    url=response.url        # URL страницы изображения для записи в CSV
                )
            else:
                self.logger.info(f"No image src found on page: {response.url}")
