from time import time
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.agents.raw_agent import run_raw_agent
from backend.agents.judge_agent import evaluate_responses
from backend.pipeline.chain import process_query,clear_history

from backend.services.session_manager import session_manager
from backend.services.batch_runner import batch_runner
from backend.services.csv_service import csv_service
from backend.services.report_store import report_store

app = FastAPI(title="PromptFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionResponse(BaseModel):
    session_id: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ClearRequest(BaseModel):
    session_id: str

class BatchRequest(BaseModel):
    queries: list[str]

@app.get("/")
def home():
    return {
        "status": "online"
    }

@app.post("/session",response_model=SessionResponse)
def create_session():
    session_id = (session_manager.create_session())
    return {"session_id":session_id}


@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    direct_start = time()
    direct_response = run_raw_agent(request.message)
    direct_time = round(time() - direct_start,2)

    direct_words = len(direct_response.split())
    direct_tokens = int(direct_words * 1.3)

    pipeline_start = time()
    pipeline_result = process_query(request.session_id,request.message)

    pipeline_time = round(time() - pipeline_start,2)
    pipeline_words = len(pipeline_result["response"].split())
    pipeline_tokens = int(pipeline_words * 1.3)

    judge_result = evaluate_responses(request.message,direct_response,pipeline_result["response"])

    result = {
        "query":
        request.message,

        "direct_response":
        direct_response,

        "refined_prompt":
        pipeline_result["refined_prompt"],

        "pipeline_response":
        pipeline_result["response"],

        "direct_stats": {
            "words":
            direct_words,

            "tokens":
            direct_tokens,

            "time":
            direct_time
        },

        "pipeline_stats": {
            "words":
            pipeline_words,

            "tokens":
            pipeline_tokens,

            "time":
            pipeline_time
        },

        **judge_result
    }

    report_store.set_result(result)
    return result


@app.post("/clear")
def clear_chat(request: ClearRequest):
    clear_history(request.session_id)
    return {
        "message":
        "Conversation cleared."
    }


@app.post("/batch/start")
def start_batch(request: BatchRequest):
    if not request.queries:
        raise HTTPException(
            status_code=400,
            detail="No queries provided."
        )

    batch_id = (batch_runner.create_batch(request.queries))

    return {
        "batch_id":
        batch_id
    }


@app.get("/batch/{batch_id}")
def get_batch_status(batch_id: str):

    batch = (batch_runner.get_status(batch_id))

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found."
        )

    return batch

@app.get("/batch/export/{batch_id}")
def export_batch(batch_id: str):
    csv_path = (batch_runner.get_csv_path(batch_id))

    if not csv_path:
        raise HTTPException(
            status_code=404,
            detail=(
                "Batch report "
                "not available."
            )
        )

    return FileResponse(
        path=csv_path,
        filename="batch_result.csv",
        media_type="text/csv"
    )


@app.get("/export/single")
def export_single():
    result = (
        report_store
        .get_result()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail=(
                "No single query "
                "result found."
            )
        )

    csv_path = (csv_service.create_single_report(result))
    return FileResponse(
        path=csv_path,
        filename="single_result.csv",
        media_type="text/csv"
    )


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }