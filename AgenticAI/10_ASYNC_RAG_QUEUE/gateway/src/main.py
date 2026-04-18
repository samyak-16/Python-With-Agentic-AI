from fastapi import FastAPI, Body, HTTPException
from config.rq import process_pdf_queue, process_query_queue

# from ...workers.src.handlers.query_handler import query_handler
from helpers.get_job_response import get_response

app = FastAPI()


@app.post("/upload-pdf")
def upload_pdf():
    pass


@app.post("/chat")
def handle_query(query: str = Body()):
    # job = process_query_queue.enqueue(query_handler, query)
    job = process_query_queue.enqueue("handlers.query_handler.query_handler", query)
    print("Job enqueued with id : ", job.id)
    return {
        "data": {
            "job_id": job.id,
        },
        "message": "Use this job_id to fetch response to the query",
    }


@app.get("/chat-response{job_id}")
def get_chat_response(job_id: str):
    try:
        data = get_response(jobId=job_id)
        if data["status"] == "queued":
            return "Still in queue try again in 5seconds"
        elif data["status"] == "started":
            return "Processing started wait for 2 seconds"

        else:
            return {"response": data["response"]}
    except Exception as e:
        raise HTTPException(500, str(e))
