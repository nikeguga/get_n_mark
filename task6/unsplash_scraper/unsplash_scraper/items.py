import scrapy

class UnsplashImageItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
