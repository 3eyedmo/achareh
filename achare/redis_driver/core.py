import redis
from django.conf import settings

redis_client = redis.Redis(
    host=settings.REFIS_CONFIG.get("HOST"),
    port=settings.REFIS_CONFIG.get("PORT")
)