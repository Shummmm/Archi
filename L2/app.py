import redis
import time

# Подключаемся к KeyDB
r = redis.Redis(host='localhost', port=6379, db=0)


# Пример cache-aside (кэширование данных из БД)
def get_data_from_db(user_id):
    print("Запрос к БД...")
    time.sleep(2)  # Имитация долгого запроса
    return {"name": "Шумский Владимир", "age": 20, "email": "shum@misis.edu"}


def get_user_data(user_id):
    cache_key = f"user:{user_id}"

    # Пытаемся получить данные из кэша
    cached_data = r.hgetall(cache_key)
    if cached_data:
        print("Данные из кэша!")
        return cached_data

    # Если нет в кэше — идём в БД
    db_data = get_data_from_db(user_id)

    # Сохраняем в кэш
    r.hset(cache_key, mapping=db_data)
    r.expire(cache_key, 60)  # TTL = 60 сек

    print("Данные из БД!")
    return db_data


# Пример использования
user_data = get_user_data(1)
print(user_data)

# При изменении данных — удаляем из кэша
r.delete("user:1")
