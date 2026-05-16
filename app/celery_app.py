from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "crypto_prices",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    imports=("app.tasks.price_tasks",),
    beat_schedule={
        "fetch-prices-every-minute": {
            "task": "app.tasks.price_tasks.fetch_and_save_prices_task",
            "schedule": crontab(minute="*"),
        },
    },
)
