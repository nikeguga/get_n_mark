from scrapy.pipelines.images import ImagesPipeline
import csv
import os
import scrapy

class UnsplashImagePipeline(ImagesPipeline):
    
    def open_spider(self, spider):
        # Открываем CSV файл для записи
        csv_file_path = r'C:\Users\User\Desktop\Get_n_mark_data\task6\output.csv'
        self.csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        # Записываем заголовки
        self.csv_writer.writerow(['URL', 'Local Path', 'Title'])

    def close_spider(self, spider):
        # Закрываем CSV файл
        self.csv_file.close()

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        # Полное имя файла с сохранённым изображением
        local_path = f"{item['title']}.jpg"
        # Возвращаем локальный путь
        return local_path

    def item_completed(self, results, item, info):
        # Проверяем, успешно ли загружено изображение
        if results and results[0][0]:
            # Локальный путь к файлу изображения
            local_path = os.path.join(self.store.basedir, results[0][1]['path'])
            # Записываем URL, локальный путь и название в CSV
            self.csv_writer.writerow([item['url'], local_path, item['title']])
        return item
