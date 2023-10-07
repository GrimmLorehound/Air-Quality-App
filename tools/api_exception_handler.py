from functools import wraps
from typing import Any, Callable

from requests import HTTPError


def handle_api_exceptions(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except Exception as unknown_error:
            print(f"An error occurred: {unknown_error}")
    return wrapper
