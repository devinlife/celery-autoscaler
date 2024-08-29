import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv(".env")

celery_app = Celery(
    "celery_app",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_RESULT_BACKEND"),
    include=["tasks", "custom", "cpu_limit", "memory_limit"],
)

celery_app.conf.worker_prefetch_multiplier = 0
celery_app.conf.worker_autoscaler = "custom.ResourceAutoscaler"
celery_app.conf.resource_limits = [
    {
        "class": "cpu_limit.CPULimit",
        "kwargs": {"max_load": 0.8},
        # "kwargs": {"max_load": 0.8, "min_load": 0.2},
    },
    {
        "class": "memory_limit.MemoryLimit",
        "kwargs": {"max_memory": 0.9},
    },
]
