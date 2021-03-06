

from typing import Optional

from . import redis

USER_TOKEN_FORMAT = "github_token_{user_id}"


def set_user_token(user_id: str, token: str) -> Optional[bool]:
    return redis.set(USER_TOKEN_FORMAT.format(user_id=user_id), token)


def delete_user_token(user_id: str) -> int:
    return redis.delete(USER_TOKEN_FORMAT.format(user_id=user_id))


def exists_user_token(user_id: str) -> int:
    return redis.exists(USER_TOKEN_FORMAT.format(user_id=user_id))


def get_user_token(user_id: str) -> Optional[str]:
    value = redis.get(USER_TOKEN_FORMAT.format(user_id=user_id))
    return value if value is None else value.decode()
