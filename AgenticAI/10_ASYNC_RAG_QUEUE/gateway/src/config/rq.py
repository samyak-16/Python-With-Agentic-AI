from rq import Queue
from .redis import redis_conn

process_pdf_queue = Queue("process_pdf", connection=redis_conn)
process_query_queue = Queue("process_query", connection=redis_conn)
