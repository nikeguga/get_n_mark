from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
import csv

class UnsplashImagePipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        # Открываем CSV файл для записи данных
        self.file = open('output.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        # Записываем заголовки
        self.writer.writerow(['title', 'categories', 'url', 'local_path'])

    def close_spider(self, spider):
        # Закрываем CSV файл при завершении работы паука
        self.file.close()

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        # Сохраняем изображение в подкаталоге с названием категории
        return f"{item['categories'][0] if item['categories'] else 'uncategorized'}/{item['title']}.jpg"

    def item_completed(self, results, item, info):
        # Проверяем, были ли успешно загружены изображения
        if results and results[0][0]:
            # Получаем путь к локально сохраненному изображению
            local_path = results[0][1]['path']

            # Записываем строку в CSV с необходимыми данными
            self.writer.writerow([
                item.get('title'),
                ', '.join(item.get('categories', [])),  # Преобразуем список категорий в строку
                item.get('url'),
                local_path
            ])

        return item
