"""Small executable input-assurance starter for Lab 05.

Replace the FireWatch fields and rules with assumptions that belong to your
project. The status precedence and evidence structure can stay the same.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


STATUS_RANK = {"pass": 0, "warning": 1, "error": 2}


def load_contract(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_rule(
    rule: str,
    observed: Any,
    passed: bool,
    severity: str,
    failure_action: str,
) -> dict[str, Any]:
    return {
        "rule": rule,
        "observed": observed,
        "status": "pass" if passed else severity,
        "action": "continue" if passed else failure_action,
    }


def combine_status(checks: list[dict[str, Any]]) -> str:
    """Return the most severe result: error beats warning, warning beats pass."""
    return max((check["status"] for check in checks), key=STATUS_RANK.__getitem__)


def validate_request(
    request: dict[str, Any],
    contract: dict[str, Any],
    runtime_context: dict[str, Any],
) -> dict[str, Any]:
    """Validate request-supplied fields and the loaded runtime identity.

    This starter does not open input_ref, decode bytes, inspect an array, or
    construct the final model tensor. The observations below are therefore
    declared request metadata unless the project replaces them with values
    measured by a trusted upstream component.
    """
    checks = [
        evaluate_rule(
            "input_reference_present",
            request.get("input_ref"),
            bool(request.get("input_ref")),
            "error",
            contract["error_action"],
        ),
        evaluate_rule(
            "format_allowed",
            request.get("format"),
            request.get("format") in contract["allowed_formats"],
            "error",
            contract["error_action"],
        ),
        evaluate_rule(
            "dimensions_supported",
            {"width": request.get("width"), "height": request.get("height")},
            isinstance(request.get("width"), int)
            and isinstance(request.get("height"), int)
            and request["width"] >= contract["minimum_width"]
            and request["height"] >= contract["minimum_height"],
            "error",
            contract["error_action"],
        ),
        evaluate_rule(
            "source_declared",
            request.get("source_id"),
            request.get("source_id") in contract["allowed_sources"],
            "warning",
            contract["warning_action"],
        ),
        evaluate_rule(
            "deployed_transform_matches",
            runtime_context.get("transform_id"),
            runtime_context.get("transform_id") == contract["transform_id"],
            "error",
            contract["error_action"],
        ),
    ]

    status = combine_status(checks)
    action = {
        "pass": "continue_to_prediction",
        "warning": contract["warning_action"],
        "error": contract["error_action"],
    }[status]

    return {
        "request_id": request["request_id"],
        "status": status,
        "action": action,
        "contract_version": contract["contract_version"],
        "model_package": runtime_context["model_package"],
        "transform_id": runtime_context["transform_id"],
        "checks": checks,
    }


def route_request(
    request: dict[str, Any],
    validation: dict[str, Any],
    predict: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Only a passing request reaches prediction in this Lab."""
    prediction_called = validation["status"] == "pass"
    prediction = predict(request) if prediction_called else None
    return {
        **validation,
        "prediction_called": prediction_called,
        "prediction": prediction,
    }
