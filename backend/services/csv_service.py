import csv
import os
from datetime import datetime

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


class CSVService:
    def create_single_report(self, result: dict) -> str:
        filename = (f"single_result_"f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        filepath = os.path.join(EXPORT_DIR, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Query",

                "Direct Response",
                "Refined Prompt",
                "Pipeline Response",

                "Direct Words",
                "Direct Tokens",
                "Direct Time (s)",

                "Pipeline Words",
                "Pipeline Tokens",
                "Pipeline Time (s)",

                "Direct Relevance",
                "Direct Clarity",
                "Direct Completeness",
                "Direct Actionability",
                "Direct Structure",
                "Direct Depth",

                "Pipeline Relevance",
                "Pipeline Clarity",
                "Pipeline Completeness",
                "Pipeline Actionability",
                "Pipeline Structure",
                "Pipeline Depth",

                "Overall Improvement (%)",
                "Winner",
                "Reason"
            ])

            left = result.get("left_metrics", {})
            right = result.get("right_metrics", {})

            direct_stats = result.get(
                "direct_stats",
                {}
            )

            pipeline_stats = result.get(
                "pipeline_stats",
                {}
            )

            writer.writerow([
                result.get("query", ""),

                result.get("direct_response", ""),
                result.get("refined_prompt", ""),
                result.get("pipeline_response", ""),

                direct_stats.get("words", ""),
                direct_stats.get("tokens", ""),
                direct_stats.get("time", ""),

                pipeline_stats.get("words", ""),
                pipeline_stats.get("tokens", ""),
                pipeline_stats.get("time", ""),

                left.get("relevance", ""),
                left.get("clarity", ""),
                left.get("completeness", ""),
                left.get("actionability", ""),
                left.get("structure", ""),
                left.get("depth", ""),

                right.get("relevance", ""),
                right.get("clarity", ""),
                right.get("completeness", ""),
                right.get("actionability", ""),
                right.get("structure", ""),
                right.get("depth", ""),

                result.get("overall_improvement", 0),
                result.get("winner", ""),
                result.get("reason", "")
            ])

        return filepath

    def create_batch_report(self, results: list) -> str:
        filename = (f"batch_result_"f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        filepath = os.path.join(EXPORT_DIR, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Sr No",
                "Query",
                "Direct Response",
                "Refined Prompt",
                "Pipeline Response",
                "Direct Words",
                "Direct Tokens",
                "Direct Time (s)",
                "Pipeline Words",
                "Pipeline Tokens",
                "Pipeline Time (s)",
                "Direct Relevance",
                "Direct Clarity",
                "Direct Completeness",
                "Direct Actionability",
                "Direct Structure",
                "Direct Depth",
                "Pipeline Relevance",
                "Pipeline Clarity",
                "Pipeline Completeness",
                "Pipeline Actionability",
                "Pipeline Structure",
                "Pipeline Depth",
                "Overall Improvement (%)",
                "Winner",
                "Reason"
            ])

            for index, result in enumerate(results, start=1):
                left = result.get(
                    "left_metrics",
                    {}
                )
                right = result.get(
                    "right_metrics",
                    {}
                )
                direct_stats = result.get(
                    "direct_stats",
                    {}
                )
                pipeline_stats = result.get(
                    "pipeline_stats",
                    {}
                )

                writer.writerow([
                    index,
                    result.get("query", ""),

                    result.get("direct_response", ""),
                    result.get("refined_prompt", ""),
                    result.get("pipeline_response", ""),

                    direct_stats.get("words", ""),
                    direct_stats.get("tokens", ""),
                    direct_stats.get("time", ""),

                    pipeline_stats.get("words", ""),
                    pipeline_stats.get("tokens", ""),
                    pipeline_stats.get("time", ""),

                    left.get("relevance", ""),
                    left.get("clarity", ""),
                    left.get("completeness", ""),
                    left.get("actionability", ""),
                    left.get("structure", ""),
                    left.get("depth", ""),

                    right.get("relevance", ""),
                    right.get("clarity", ""),
                    right.get("completeness", ""),
                    right.get("actionability", ""),
                    right.get("structure", ""),
                    right.get("depth", ""),

                    result.get("overall_improvement", 0),
                    result.get("winner", ""),
                    result.get("reason", "")
                ])
        return filepath

csv_service = CSVService()