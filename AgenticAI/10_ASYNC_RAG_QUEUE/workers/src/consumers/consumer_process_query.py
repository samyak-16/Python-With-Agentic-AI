from rq import SimpleWorker
from config.redis import redis_conn


def start():
    worker = SimpleWorker(
        ["process_query"], name="query_worker", connection=redis_conn
    )
    print("Worker started, listening on queue : process_query")
    worker.work()
