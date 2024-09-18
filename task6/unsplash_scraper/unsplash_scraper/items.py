import scrapy

class UnsplashImageItem(scrapy.Item):
    title = scrapy.Field()        # Название изображения (alt)
    image_urls = scrapy.Field()   # URL изображения
    images = scrapy.Field()       # Стандартное поле для ImagesPipeline
    url = scrapy.Field()          # URL страницы изображения для записи в CSV
