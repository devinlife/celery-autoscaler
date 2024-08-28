import time

from celery import Task
from sentence_transformers import SentenceTransformer

from celery_worker import celery_app


class PredictTask(Task):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            print("Loading model")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self._cpu_stress(10)

        return self.run(*args, **kwargs)

    def _cpu_stress(self, duration_seconds):
        end_time = time.time() + duration_seconds
        print("start")
        while time.time() < end_time:
            pass
        print("end")


@celery_app.task(ignore_result=False, bind=True, base=PredictTask, name="model")
def predict(self, sentences):
    print("Celery task started")
    embeddings = self.model.encode(sentences).tolist()
    res = dict(zip(sentences, embeddings))
    return res
