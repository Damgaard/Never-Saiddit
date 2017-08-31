from .celery import app

@app.task(bind=True)
def debug_task_2(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
