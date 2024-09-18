from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os

class UnsplashImagePipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        return f"{item['category']}/{item['title']}.jpg"
