

import pickle
import inspect
from functools import wraps
from datetime import timedelta
from typing import Any, Optional, TypeVar, Callable

import redis
import nonebot
from nonebot import get_driver

from .config import Config

CACHE_KEY_FORMAT = "cache_{signature}"

global_config = get_driver().config
redis_config = Config(**global_config.dict())

redis_client = redis.Redis(redis_config.redis_host,
                           redis_config.redis_port,
                           redis_config.redis_db,
                           charset="utf-8",
                           password=redis_config.redis_password,
                           username=redis_config.redis_username)


def gen_signature(args, kwds, kwd_mark=(object(),)) -> int:
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item
    return hash(key)


def get_cache(sign: str) -> Any:
    cache = redis_client.get(CACHE_KEY_FORMAT.format(signature=sign))
    return pickle.loads(cache) if cache else cache


def save_cache(sign: str, cache: Any, ex: Optional[timedelta] = None) -> None:
    redis_client.set(CACHE_KEY_FORMAT.format(signature=sign),
                     pickle.dumps(cache), ex)


# Export something for other plugin
export = nonebot.export()
export.redis = redis_client

F = TypeVar("F", bound=Callable[..., Any])


@export
def cache(ex: Optional[timedelta] = None) -> Callable[[F], F]:

    def decorator(func: F) -> F:

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                key = str(gen_signature(args, kwargs))
                result = get_cache(key)
                if not result:
                    result = await func(*args, **kwargs)
                    save_cache(key, result, ex)
                return result

            return async_wrapper  # type: ignore

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                key = str(gen_signature(args, kwargs))
                result = get_cache(key)
                if not result:
                    result = func(*args, **kwargs)
                    save_cache(key, result)
                return result

            return wrapper  # type: ignore

    return decorator
