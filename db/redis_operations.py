import json
from typing import Any, List

from db.redis import redis_client


class Redis:

    def get(self, key: str) -> Any | None:
        data = redis_client.get(name=key)
        if not data:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any) -> None:
        data = json.dumps(value)
        redis_client.set(name=key, value=data)

    def rpush(self, key: str, value: Any) -> None:
        data = json.dumps(value)
        redis_client.rpush(name=key, value=data)

    def replace(self, key: str, value: Any) -> None:
        self.delete_one(keys=key)
        data = json.dumps(value)
        redis_client.set(name=key, value=data)

    def delete_one(self, keys: List[str] | str) -> None:
        redis_client.delete(*keys)

    def delete_all(self, key: str) -> None:
        keys = redis_client.keys(f"{key}*")
        if keys:
            redis_client.delete(*keys)


db = Redis()
