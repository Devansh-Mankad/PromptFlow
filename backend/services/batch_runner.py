import threading
import time
import uuid

from backend.agents.raw_agent import run_raw_agent
from backend.pipeline.chain import process_query
from backend.agents.judge_agent import evaluate_responses
from backend.services.csv_service import csv_service

BATCH_PAUSE_SECONDS = 60

class BatchRunner:
    def __init__(self):
        self.batches = {}

    def create_batch(self, queries: list[str]) -> str:
        batch_id = str(uuid.uuid4())

        self.batches[batch_id] = {
            "status": "queued",
            "queries": queries,
            "results": [],
            "current_index": 0,
            "total_queries": len(queries),
            "latest_result": None,
            "countdown": 0,
            "csv_path": None
        }

        thread = threading.Thread(
            target=self._run_batch,
            args=(batch_id,),
            daemon=True
        )

        thread.start()
        return batch_id

    def _run_batch(self, batch_id: str):
        batch = self.batches[batch_id]
        batch["status"] = "Running"

        try:
            for index, query in enumerate(batch["queries"], start=1):
                batch["current_index"] = index
                session_id = str(uuid.uuid4())

                direct_start = time.time()
                direct_response = run_raw_agent(query)
                direct_time = round(time.time() - direct_start, 2)

                direct_words = len(direct_response.split())
                direct_tokens = int(direct_words * 1.3)

                pipeline_start = time.time()
                pipeline_result = process_query(session_id,query)
                pipeline_time = round(
                    time.time() - pipeline_start,
                    2
                )

                pipeline_words = len(
                    pipeline_result["response"].split()
                )

                pipeline_tokens = int(
                    pipeline_words * 1.3
                )

                judge_result = evaluate_responses(
                    query,
                    direct_response,
                    pipeline_result["response"]
                )

                result = {
                    "query": query,

                    "direct_response": direct_response,

                    "refined_prompt":
                    pipeline_result["refined_prompt"],

                    "pipeline_response":
                    pipeline_result["response"],

                    "direct_stats": {
                        "words": direct_words,
                        "tokens": direct_tokens,
                        "time": direct_time
                    },

                    "pipeline_stats": {
                        "words": pipeline_words,
                        "tokens": pipeline_tokens,
                        "time": pipeline_time
                    },

                    **judge_result
                }

                batch["latest_result"] = result
                batch["results"].append(result)

                if index < len(batch["queries"]):
                    for sec in range(
                        BATCH_PAUSE_SECONDS,
                        0,
                        -1
                    ):
                        batch["countdown"] = sec
                        time.sleep(1)

                batch["countdown"] = 0

            csv_path = csv_service.create_batch_report(
                batch["results"]
            )

            batch["csv_path"] = csv_path
            batch["status"] = "Completed"
            batch["countdown"] = 0

        except Exception as e:
            batch["status"] = "Failed"
            batch["error"] = str(e)

    def get_status(self, batch_id: str):
        return self.batches.get(batch_id)

    def get_csv_path(self, batch_id: str):
        batch = self.batches.get(batch_id)
        if not batch:
            return None
        return batch.get("csv_path")

batch_runner = BatchRunner()