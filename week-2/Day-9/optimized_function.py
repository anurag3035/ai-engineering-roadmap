from functools import lru_cache
import time


def slow_fibonacci(n):
    if n <= 1:
        return n

    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


@lru_cache(maxsize=None)
def fast_fibonacci(n):
    if n <= 1:
        return n

    return fast_fibonacci(n - 1) + fast_fibonacci(n - 2)


start = time.time()
result = slow_fibonacci(35)
end = time.time()

print("Slow Fibonacci Result:", result)
print("Execution Time:", round(end - start, 4), "seconds")

print("-" * 40)

start = time.time()
result = fast_fibonacci(35)
end = time.time()

print("Optimized Fibonacci Result:", result)
print("Execution Time:", round(end - start, 4), "seconds")