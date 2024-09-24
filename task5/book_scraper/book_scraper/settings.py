BOT_NAME = "book_scraper"

SPIDER_MODULES = ["book_scraper.spiders"]
NEWSPIDER_MODULE = "book_scraper.spiders"

# Ротация User-Agent'ов для обхода блокировок
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
]

# Не соблюдать правила robots.txt
ROBOTSTXT_OBEY = False

# Задержка между запросами для одного домена
DOWNLOAD_DELAY = 2

# Максимальное количество запросов к одному домену
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Включение повторных попыток запросов при ошибках
RETRY_ENABLED = True
RETRY_TIMES = 3  # Количество повторных попыток

# Отключаем cookies для защиты от отслеживания
COOKIES_ENABLED = False

# Таймаут запросов (в секундах)
DOWNLOAD_TIMEOUT = 15

# Логирование
LOG_LEVEL = 'INFO'

# Конфигурация экспорта данных в JSON Lines
FEEDS = {
    'C:/Users/User/Desktop/Get_n_mark_data/tsak_5/books.json': {
        'format': 'jsonlines',  # Формат jsonlines
        'encoding': 'utf8',     # Кодировка
        'store_empty': False,   # Не сохранять пустые файлы
        'indent': 0,            # Минимальные отступы
    },
}

# Использование Twisted для асинхронного выполнения
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Дополнительные заголовки для обхода блокировок
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Referer': 'https://www.google.com/',  # Имитация перехода с Google
}
