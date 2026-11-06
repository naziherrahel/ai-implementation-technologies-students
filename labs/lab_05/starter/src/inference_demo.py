"""Run three request-level validation cases and save the JSONL trace."""

from __future__ import annotations

import json
from pathlib import Path

from input_validation import load_contract, route_request, validate_request


# In a real service, load these values from the deployed model package manifest
# at startup. The request itself does not certify the running transform.
RUNTIME_CONTEXT = {
    "model_package": "firewatch-smoke-v4",
    "transform_id": "sha256:5639361c0370",
}

CASES = [
    {
        "request_id": "req-001",
        "input_ref": "frames/camera-a-001.jpg",
        "format": "jpg",
        "width": 1280,
        "height": 720,
        "source_id": "camera-a",
    },
    {
        "request_id": "req-002",
        "input_ref": "frames/camera-c-002.gif",
        "format": "gif",
        "width": 160,
        "height": 120,
        "source_id": "camera-c",
    },
    {
        "request_id": "req-003",
        "input_ref": "frames/camera-c-003.jpg",
        "format": "jpg",
        "width": 1280,
        "height": 720,
        "source_id": "camera-c",
    },
]


def project_predict_stub(_: dict[str, object]) -> dict[str, object]:
    """Prove the call boundary; this is not an actual model inference.

    In the team project, keep the working Lab 04 prediction function and call
    it here, for example with request["input_ref"].
    """
    return {"result": "prediction_stub_called"}


def main() -> None:
    contract = load_contract("config/input_contract.json")
    output_path = Path("reports/validation_demo.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for request in CASES:
        validation = validate_request(request, contract, RUNTIME_CONTEXT)
        records.append(route_request(request, validation, project_predict_stub))

    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")

    for record in records:
        print(
            record["request_id"],
            record["status"],
            record["action"],
            f"prediction_called={record['prediction_called']}",
        )
    print(f"Wrote {len(records)} records to {output_path}")


if __name__ == "__main__":
    main()
