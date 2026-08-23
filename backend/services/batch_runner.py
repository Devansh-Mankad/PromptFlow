import threading
import time
import uuid
import traceback
from copy import deepcopy
from backend.agents.raw_agent import run_raw_agent
from backend.pipeline.chain import process_query, clear_history
from backend.agents.judge_agent import evaluate_responses
from backend.services.csv_service import csv_service

BATCH_PAUSE_SECONDS = 60
_BATCH_LOCK = threading.Lock()

class BatchRunner:
    def __init__(self):
        self.batches = {}
        self._state_lock = threading.RLock()

    def create_batch(self, queries: list[str]) -> str:
        if not queries:
            raise ValueError("Batch cannot be empty.")

        if _BATCH_LOCK.locked():
            raise RuntimeError("Another benchmark batch is already running.")
        
        batch_id = str(uuid.uuid4())
        with self._state_lock:
            self.batches[batch_id] = {
                "status": "queued",
                "queries": list(queries),
                "results": [],
                "current_index": 0,
                "total_queries": len(queries),
                "latest_result": None,
                "countdown": 0,
                "csv_path": None,
                "error": None,
                "started_at": None,
                "completed_at": None,
            }

        thread = threading.Thread(
            target=self._run_batch,
            args=(batch_id,),
            daemon=True,
            name=f"PromptFlow-Batch-{batch_id[:8]}"
        )
        thread.start()
        return batch_id

    def _update(self, batch_id: str, **values):
        with self._state_lock:
            batch = self.batches.get(batch_id)
            if batch is None:
                return
            batch.update(values)

    def _run_batch(self, batch_id: str):
        acquired = _BATCH_LOCK.acquire(blocking=False)
        if not acquired:
            self._update(
                batch_id,
                status="Failed",
                error=(
                    "Another benchmark is already using "
                    "the shared model."
                )
            )
            return

        try:
            self._update(batch_id,status="Running",started_at=time.time())
            batch = self.batches[batch_id]
            queries = list(batch["queries"])
            total = len(queries)

            print("\n")
            print("PROMPTFLOW BATCH BENCHMARK STARTED")
            print(f"Batch ID: {batch_id}")
            print(f"Total queries: {total}")
            print("\n")

            for index, query in enumerate(queries,start=1):
                query = query.strip()
                self._update(
                    batch_id,
                    current_index=index,
                    countdown=0
                )

                print("\n")
                print(f"BATCH QUERY {index}/{total}")
                print("\nRAW QUERY:")
                print(query)

                session_id = str(uuid.uuid4())

                print("\nSESSION:")
                print(session_id)

                direct_response = None
                refined_prompt = None
                pipeline_response = None

                direct_time = 0.0
                pipeline_time = 0.0

                try:
                    print("\n[1/3] Running direct Gemma 4 baseline...")
                    direct_start = time.perf_counter()
                    direct_response = run_raw_agent(query)
                    direct_time = round(time.perf_counter()- direct_start,2)
                    print(f"Direct response generated "f"in {direct_time}s")

                    print("\n[2/3] Running Agent 1 → Agent 2...")
                    pipeline_start = time.perf_counter()
                    pipeline_result = process_query(session_id,query)

                    pipeline_time = round(time.perf_counter()- pipeline_start,2)
                    refined_prompt = str(pipeline_result.get("refined_prompt",""))
                    pipeline_response = str(pipeline_result.get("response",""))

                    print(f"Pipeline generated "f"in {pipeline_time}s")
                    print("\nAGENT 1 REFINED PROMPT:")
                    print(refined_prompt)

                    print("\n[3/3] Running Judge...")

                    judge_result = evaluate_responses(
                        query,
                        direct_response,
                        pipeline_response
                    )

                    judge_result = deepcopy(judge_result)

                    print("\nJUDGE RESULT:")
                    print(judge_result)


                    direct_words = len(direct_response.split())
                    pipeline_words = len(pipeline_response.split())
                    direct_tokens = int(direct_words * 1.3)
                    pipeline_tokens = int(pipeline_words * 1.3)

                    result = {
                        "query": query,
                        "direct_response":direct_response,
                        "refined_prompt":refined_prompt,
                        "pipeline_response":pipeline_response,

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

                        **judge_result,

                        "benchmark_metadata": {
                            "batch_id": batch_id,
                            "query_index": index,
                            "session_id": session_id
                        }
                    }

                    with self._state_lock:
                        batch["results"].append(deepcopy(result))
                        batch["latest_result"] = (deepcopy(result))
                    print(
                        f"\n✓ Query {index}/{total} "
                        f"completed successfully."
                    )

                except Exception as query_error:
                    print("\n")
                    print("QUERY FAILED")
                    print(str(query_error))
                    traceback.print_exc()

                    failure_result = {
                        "query": query,
                        "direct_response":
                            direct_response or "",
                        "refined_prompt":
                            refined_prompt or "",
                        "pipeline_response":
                            pipeline_response or "",
                        "error": str(query_error),
                        "benchmark_metadata": {
                            "batch_id": batch_id,
                            "query_index": index,
                            "session_id": session_id
                        }
                    }

                    with self._state_lock:
                        batch["results"].append(deepcopy(failure_result))
                        batch["latest_result"] = (deepcopy(failure_result))

                if index < total:
                    print(f"\nWaiting "f"{BATCH_PAUSE_SECONDS}s "f"before next query...")
                    for remaining in range(BATCH_PAUSE_SECONDS,0,-1):
                        self._update(batch_id,countdown=remaining)
                        time.sleep(1)

                self._update(batch_id,countdown=0)

            print("\n")
            print("CREATING FINAL BATCH REPORT")

            with self._state_lock:
                final_results = deepcopy(batch["results"])

            csv_path = csv_service.create_batch_report(final_results)
            self._update(
                batch_id,
                csv_path=csv_path,
                status="Completed",
                countdown=0,
                completed_at=time.time()
            )

            print("\n")
            print("BATCH COMPLETED")
            print(f"Batch ID: {batch_id}")
            print(f"Results: {len(final_results)}")
            print(f"CSV: {csv_path}")

        except Exception as e:
            print("\n")
            print("BATCH FAILED")
            traceback.print_exc()
            self._update(
                batch_id,
                status="Failed",
                error=str(e),
                countdown=0,
                completed_at=time.time()
            )
        finally:
            _BATCH_LOCK.release()

    def get_status(self, batch_id: str):
        with self._state_lock:
            batch = self.batches.get(batch_id)
            if batch is None:
                return None
            return deepcopy(batch)

    def get_csv_path(self, batch_id: str):
        with self._state_lock:
            batch = self.batches.get(batch_id)
            if not batch:
                return None
            return batch.get("csv_path")

batch_runner = BatchRunner()