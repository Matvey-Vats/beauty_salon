from django.core.cache import cache

class CacheMixin:
    """
    Миксин для кэширования данных в представлениях Django.
    """
    def get_cache_data(self, cache_name):
        """Получаем данные из кэша"""
        data = cache.get(cache_name)
        if data:
            print(f"Cache hit for {cache_name}. Returning cached data.")  # Логирование для отладки
        else:
            print(f"Cache miss for {cache_name}. Fetching from database.")  # Логирование для отладки
        return data

    def set_cache_data(self, cache_name, data, cache_time):
        """Сохраняем данные в кэше"""
        cache.set(cache_name, data, cache_time)
        print(f"Data cached with key: {cache_name} for {cache_time} seconds.")  # Логирование для отладки

    def invalidate_cache(self, cache_name):
        """Удаляем кэшированные данные"""
        cache.delete(cache_name)
        print(f"Cache invalidated for {cache_name}.")  # Логирование для отладки
