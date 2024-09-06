import requests

# Введите сюда ваш Foursquare API-ключ
API_KEY = 'ВАШ_API_КЛЮЧ_FOURSQUARE'

# URL для Foursquare Places API
API_URL = "https://api.foursquare.com/v3/places/search"

# Функция для получения данных о заведениях по заданным параметрам
def search_places(query, city, min_rating, limit=10):
    headers = {
        "Accept": "application/json",
        "Authorization": API_KEY
    }
    
    # Параметры для запроса
    params = {
        "query": query,
        "near": city,
        "limit": limit,
        "sort": "relevance"  # Сортировка по релевантности
    }

    response = requests.get(API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        places = response.json()["results"]
        filtered_places = []
        
        # Фильтруем заведения по минимальному рейтингу
        for place in places:
            rating = place.get("rating", 0)  # Если нет рейтинга, то по умолчанию 0
            if rating >= min_rating:
                filtered_places.append(place)
        
        return filtered_places
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return []

# Функция для отображения информации о заведениях
def display_places(places):
    if not places:
        print("Заведений не найдено, совсем.")
        return
    
    for i, place in enumerate(places, 1):
        name = place.get('name', 'Название неизвестно')
        address = ', '.join(place['location'].get('formatted_address', 'Адрес неизвестен'))
        rating = place.get('rating', 'Нет рейтинга')
        print(f"{i}. {name}\n   Адрес: {address}\n   Рейтинг: {rating}\n")

# Основная программа
if __name__ == "__main__":
    print("Вэлкам в Foursquare!")
    
    # Ввод категории (тип заведения)
    query = input("Введите категорию интересующего заведения (например, кафе, парки, музеи): ").strip()
    
    # Ввод города
    city = input("Введите город для поиска: ").strip()
    
    # Ввод минимального рейтинга
    min_rating = float(input("Введите минимальный рейтинг заведения (от 0 до 10): ").strip())
    
    # Ввод ограничения количества заведений (например, 10)
    limit = int(input("Сколько заведений показать? (например, 10): ").strip())
    
    # Поиск заведений с заданными параметрами
    places = search_places(query, city, min_rating, limit)
    
    # Вывод заведений
    display_places(places)
