from contextlib import contextmanager
from typing import List

import redis
from django.conf import settings
from django.core.mail import EmailMessage


class EmailService:
    def smtp(self, subject, body, to: List[str]):
        email = EmailMessage(subject, body, to=to)
        email.send()


class RedisService:
    @contextmanager
    def connect(self) -> redis.Redis:
        rds = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            charset="utf-8",
            decode_responses=True,
        )

        try:
            yield rds
        finally:
            rds.close()

    def set(self, key, value, expire=None):
        with self.connect() as conn:
            conn.set(key, value)
            if expire:
                conn.expire(key, expire)

    def get(self, key):
        with self.connect() as conn:
            return conn.get(key)

    def delete(self, key):
        with self.connect() as conn:
            conn.delete(key)
