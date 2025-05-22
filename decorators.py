# decorators.py
import time
from functools import wraps

def timer(func):
    """测量函数执行时间的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__!r} executed in {(end_time - start_time):.4f}s")
        return result
    return wrapper

def retry(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Attempt {retries} failed with error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {max_retries} attempts")
        return wrapper
    return decorator

def deprecated(reason=None):
    """标记函数为已弃用的装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            message = f"Function {func.__name__} is deprecated"
            if reason:
                message += f": {reason}"
            print(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@timer
def example_function(n):
    """模拟耗时函数"""
    time.sleep(n)
    return f"Slept for {n} seconds"

@retry(max_retries=2, delay=0.5)
def might_fail():
    """可能失败的函数"""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return "Success"

@deprecated("Use new_function() instead")
def old_function():
    return "This is old"

if __name__ == "__main__":
    print(example_function(1))
    try:
        print(might_fail())
    except Exception as e:
        print(f"Final failure: {e}")
    print(old_function())