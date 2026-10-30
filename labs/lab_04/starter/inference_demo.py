"""Lab 04 starter: connect one project input to a traceable response.

Copy this file to ``src/inference_demo.py`` in the team repository. Replace the
marked project-specific values and ``project_predict`` implementation.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any
from uuid import uuid4


MODEL_VERSION = "baseline-v1"
RULE_VERSION = "decision-v1"

# Replace these actions with the decisions made by your team in Lab 03.
NORMAL_ACTION = "REPLACE_WITH_NORMAL_USER_ACTION"
REVIEW_ACTION = "REPLACE_WITH_MANUAL_CHECK_ACTION"
UNAVAILABLE_ACTION = "REPLACE_WITH_SAFE_UNAVAILABLE_ACTION"


def project_predict(input_ref: str) -> dict[str, Any]:
    """Return one prediction by reusing the Lab 02 baseline code.

    Expected shape:
        {"result": "project-specific result", "needs_review": False}

    Import or adapt the prediction step that already exists in your project.
    Do not leave a hard-coded prediction here.
    """

    raise NotImplementedError("Connect project_predict() to the Lab 02 baseline")


def run_attempt(input_ref: str, *, simulate_unavailable: bool) -> dict[str, Any]:
    started = time.perf_counter()

    if simulate_unavailable:
        status = "unavailable"
        result = None
        action = UNAVAILABLE_ACTION
    else:
        prediction = project_predict(input_ref)
        result = prediction["result"]
        needs_review = bool(prediction.get("needs_review", False))
        status = "review" if needs_review else "ok"
        action = REVIEW_ACTION if needs_review else NORMAL_ACTION

    return {
        "request_id": str(uuid4()),
        "input_ref": input_ref,
        "status": status,
        "result": result,
        "model_version": MODEL_VERSION,
        "rule_version": RULE_VERSION,
        "latency_ms": round((time.perf_counter() - started) * 1000, 1),
        "action": action,
        "simulated": simulate_unavailable,
    }


def write_evidence(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-ref", required=True, help="Path, row ID, or other safe input reference")
    parser.add_argument("--output", default="reports/inference_demo.jsonl")
    args = parser.parse_args()

    records = [
        run_attempt(args.input_ref, simulate_unavailable=False),
        run_attempt(args.input_ref, simulate_unavailable=True),
    ]
    output = Path(args.output)
    write_evidence(records, output)

    for record in records:
        print(json.dumps(record, ensure_ascii=False))
    print(f"Saved {len(records)} records to {output}")


if __name__ == "__main__":
    main()
