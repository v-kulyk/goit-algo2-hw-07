import time
import random
from collections import OrderedDict
from collections import defaultdict

# Функції без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

# Клас для LRU-кешу
class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.index_map = defaultdict(set)
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value, L, R):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                oldest = next(iter(self.cache))
                del self.cache[oldest]
                for i in range(oldest[0], oldest[1]+1):
                    self.index_map[i].discard(oldest)
            for i in range(L, R+1):
                self.index_map[i].add(key)
        self.cache[key] = value

    def invalidate(self, index):
        if index in self.index_map:
            ranges = list(self.index_map[index])
            for r in ranges:
                if r in self.cache:
                    del self.cache[r]
            del self.index_map[index]

# Глобальний кеш
cache = LRUCache(1000)

# Функції з кешем
def range_sum_with_cache(array, L, R):
    key = (L, R)
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = sum(array[L:R+1])
    cache.put(key, result, L, R)
    return result

def update_with_cache(array, index, value):
    array[index] = value
    cache.invalidate(index)

# Тестування
def main():
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []

    # Генерація запитів
    for _ in range(Q):
        if random.random() < 0.8:  # 80% Range, 20% Update
            L = random.randint(0, N-1)
            R = random.randint(L, N-1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N-1)
            value = random.randint(1, 100)
            queries.append(('Update', index, value))

    # Тест без кешу
    arr_no_cache = array.copy()
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(arr_no_cache, query[1], query[2])
        else:
            update_no_cache(arr_no_cache, query[1], query[2])
    time_no_cache = time.time() - start

    # Тест з кешем
    arr_with_cache = array.copy()
    start = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(arr_with_cache, query[1], query[2])
        else:
            update_with_cache(arr_with_cache, query[1], query[2])
    time_with_cache = time.time() - start

    print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")

if __name__ == "__main__":
    main()