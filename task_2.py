import sys
sys.setrecursionlimit(10000)

from functools import lru_cache
import timeit
import matplotlib.pyplot as plt

# Реалізація Splay Tree
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root = self._insert(self.root, key, value)
        self.splay(self.root)

    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
            node.left.parent = node
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
            node.right.parent = node
        else:
            node.value = value
        return node

    def search(self, key):
        node = self._search(self.root, key)
        if node:
            self.splay(node)
            return node.value
        return None

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def splay(self, node):
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                if node == parent.left:
                    self.right_rotate(parent)
                else:
                    self.left_rotate(parent)
            else:
                if parent.left == node and grandparent.left == parent:
                    self.right_rotate(grandparent)
                    self.right_rotate(parent)
                elif parent.right == node and grandparent.right == parent:
                    self.left_rotate(grandparent)
                    self.left_rotate(parent)
                elif parent.right == node and grandparent.left == parent:
                    self.left_rotate(parent)
                    self.right_rotate(grandparent)
                else:
                    self.right_rotate(parent)
                    self.left_rotate(grandparent)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

# Функції для обчислення Фібоначчі
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def fibonacci_splay(n, tree):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    cached = tree.search(n)
    if cached is not None:
        return cached
    fib = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, fib)
    return fib

# Генерація списку n
n_values = list(range(0, 951, 50))

# Вимірювання часу для LRU
lru_times = []
for n in n_values:
    time_taken = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(time_taken)

# Вимірювання часу для Splay Tree
splay_times = []
tree = SplayTree()
for n in n_values:
    time_taken = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
    splay_times.append(time_taken)

# Виведення таблиці
print("n         LRU Cache Time (s)  Splay Tree Time (s)")
print("--------------------------------------------------")
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(f"{n:<9} {lru:.8f}          {splay:.8f}")

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache', marker='o')
plt.plot(n_values, splay_times, label='Splay Tree', marker='x')
plt.xlabel('n')
plt.ylabel('Час (секунди)')
plt.title('Порівняння часу обчислення чисел Фібоначчі')
plt.legend()
plt.grid(True)
plt.show()