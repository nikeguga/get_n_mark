import scrapy

class UnsplashImageItem(scrapy.Item):
    title = scrapy.Field()        # Название изображения (alt)
    category = scrapy.Field()     # Категории изображения
    image_urls = scrapy.Field()   # URL изображения
    images = scrapy.Field()       # Стандартное поле для ImagesPipeline
    file_paths = scrapy.Field()   # Локальный путь к сохраненному изображению
    image_url = scrapy.Field()    # URL изображения для записи в CSV
