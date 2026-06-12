from functools import wraps
import time


def retry(max_attempts=3, delay=1):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(max_attempts):

                try:
                    return func(*args, **kwargs)

                except Exception as e:

                    print(f"Attempt {attempt + 1} failed: {e}")

                    if attempt == max_attempts - 1:
                        raise

                    time.sleep(delay)

        return wrapper

    return decorator


def timeit(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        print(f"Execution Time: {end - start:.4f} seconds")

        return result

    return wrapper


counter = 0


@timeit
@retry(max_attempts=3, delay=1)
def mock_api():

    global counter

    counter += 1

    if counter < 3:
        raise ValueError("API request failed")

    return "API request successful"


if __name__ == "__main__":

    try:
        result = mock_api()
        print(result)

    except Exception as e:
        print(f"Error: {e}")