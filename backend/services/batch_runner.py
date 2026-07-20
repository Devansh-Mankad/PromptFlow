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

    def create_batch(self,queries: list[str]) -> str:
        batch_id = str(uuid.uuid4())

        self.batches[batch_id] = {
            "status": "queued",
            "queries": queries,
            "results": [],
            "current_index": 0,
            "total_queries": len(
                queries
            ),
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

    def _run_batch(self,batch_id: str):
        batch = self.batches[batch_id]
        batch["status"] = "running"
        session_id = (f"batch_{batch_id}")

        try:
            for index, query in enumerate(batch["queries"],start=1):
                batch["current_index"] = index

                direct_response = (run_raw_agent(query))

                pipeline_result = (process_query(session_id,query))

                judge_result = (evaluate_responses(query,direct_response,pipeline_result["response"]))

                result = {
                    "query": query,
                    "direct_response":direct_response,

                    "refined_prompt":pipeline_result["refined_prompt"],

                    "pipeline_response":pipeline_result["response"],

                    **judge_result
                }

                batch["latest_result"] = result
                batch["results"].append(result)

                if index < len(batch["queries"]):
                    for sec in range(BATCH_PAUSE_SECONDS,0,-1):
                        batch["countdown"] = sec
                        time.sleep(1)

            csv_path = (csv_service.create_batch_report(batch["results"]))

            batch["csv_path"] = csv_path
            batch["countdown"] = 0
            batch["status"] = "completed"

        except Exception as e:
            batch["status"] = "failed"
            batch["error"] = str(e)

    def get_status(self,batch_id: str):
        return self.batches.get(batch_id)

    def get_csv_path(self,batch_id: str):
        batch = self.batches.get(batch_id)
        if not batch:
            return None
        return batch.get("csv_path")

batch_runner = BatchRunner()