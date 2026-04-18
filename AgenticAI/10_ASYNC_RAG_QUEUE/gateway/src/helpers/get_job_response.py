from rq.job import Job
from config.redis import redis_conn


def get_response(jobId: str):
    job = Job.fetch(jobId, connection=redis_conn)
    status = job._status
    response = job.result
    return {"status": status, "response": response}
