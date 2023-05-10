from rest_framework.response import Response
from rest_framework import status
from .config import redis_cache, limit_time


def user_limiter(ip: str, key: str, limit_number: int, user_ip_obj):
    user_exist = redis_cache.exists(key)
    is_limit = int(redis_cache.get(key)) == limit_number if user_exist else False
    if user_exist and is_limit:
        if user_ip_obj.filter(ip=ip).exists():
            return Response(data={"detail": "Restrictions On Your Requests"}, status= status.HTTP_423_LOCKED)
    ip_cache = redis_cache.setex(key, limit_time, 0) if not user_exist or is_limit else None