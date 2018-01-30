import time


def wait_until(condition, interval=0.1, timeout=1, *args, **kwargs):
    start = time.time()
    result = condition(*args, **kwargs)
    while not result and time.time() - start < timeout:
        time.sleep(interval)
        result = condition(*args, **kwargs)
    return result