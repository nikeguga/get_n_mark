BOT_NAME = 'unsplash_scraper'

SPIDER_MODULES = ['unsplash_scraper.spiders']
NEWSPIDER_MODULE = 'unsplash_scraper.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
IMAGES_STORE = r'C:\Users\User\Desktop\Get_n_mark_data\task6\images'

DOWNLOAD_DELAY = 1
