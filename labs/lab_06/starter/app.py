"""A small, real YOLO inference API for the cloud deployment practice."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from time import perf_counter
from typing import Any, Callable
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from image_validation import all_checks_pass, load_contract, validate_image_upload


BASE_DIR = Path(__file__).resolve().parent
LOGGER = logging.getLogger(__name__)
load_dotenv(BASE_DIR / ".env")


class YoloPredictor:
    """Load the pretrained model on the first valid request."""

    def __init__(self, model_name: str, confidence: float, image_size: int) -> None:
        self.model_name = model_name
        self.confidence = confidence
        self.image_size = image_size
        self._model: Any | None = None

    @property
    def loaded(self) -> bool:
        return self._model is not None

    def __call__(self, image: Image.Image) -> dict[str, Any]:
        if self._model is None:
            from ultralytics import YOLO

            self._model = YOLO(self.model_name)

        started = perf_counter()
        result = self._model.predict(
            source=image,
            conf=self.confidence,
            imgsz=self.image_size,
            device="cpu",
            verbose=False,
        )[0]
        latency_ms = round((perf_counter() - started) * 1000, 1)

        detections: list[dict[str, Any]] = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                detections.append(
                    {
                        "class_id": class_id,
                        "class_name": result.names[class_id],
                        "confidence": round(float(box.conf.item()), 4),
                        "box_xyxy": [round(float(value), 1) for value in box.xyxy[0]],
                    }
                )

        return {
            "model": self.model_name,
            "confidence_threshold": self.confidence,
            "latency_ms": latency_ms,
            "object_count": len(detections),
            "detections": detections,
        }


def append_jsonl(record: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def create_app(
    evidence_path: Path | None = None,
    predictor: Callable[[Image.Image], dict[str, Any]] | None = None,
) -> FastAPI:
    environment = os.getenv("ENVIRONMENT", "classroom")
    service_version = os.getenv("SERVICE_VERSION", "yolo-cloud-demo-v1")
    model_name = os.getenv("MODEL_NAME", "yolo26n.pt")
    confidence = float(os.getenv("CONFIDENCE_THRESHOLD", "0.25"))
    image_size = int(os.getenv("IMAGE_SIZE", "640"))
    contract = load_contract(BASE_DIR / "config" / "input_contract.json")
    trace_path = evidence_path or BASE_DIR / os.getenv(
        "EVIDENCE_PATH", "reports/yolo_predictions.jsonl"
    )
    model_predict = predictor or YoloPredictor(model_name, confidence, image_size)

    application = FastAPI(
        title="Pretrained YOLO Cloud Demo",
        version=service_version,
        description=(
            "Upload a JPEG or PNG image. The service validates the decoded image, "
            "runs a pretrained nano YOLO model on CPU, and records the decision."
        ),
    )

    @application.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "environment": environment,
            "service_version": service_version,
            "model": model_name,
            "model_loaded": getattr(model_predict, "loaded", False),
        }

    @application.post("/predict", response_model=None)
    async def predict(
        file: UploadFile = File(...),
        request_id: str = Form(default=""),
    ) -> Any:
        resolved_request_id = request_id.strip() or f"req-{uuid4().hex[:8]}"
        maximum = int(contract["maximum_upload_bytes"])
        data = await file.read(maximum + 1)
        checks, image, image_metadata = validate_image_upload(
            data,
            file.content_type,
            contract,
        )

        base_record: dict[str, Any] = {
            "request_id": resolved_request_id,
            "filename": file.filename,
            "status": "pass" if all_checks_pass(checks) else "error",
            "action": (
                "continue_to_prediction"
                if all_checks_pass(checks)
                else contract["error_action"]
            ),
            "contract_version": contract["contract_version"],
            "image": image_metadata,
            "checks": checks,
        }

        if image is None or not all_checks_pass(checks):
            record = {
                **base_record,
                "prediction_called": False,
                "prediction": None,
            }
            append_jsonl(record, trace_path)
            return JSONResponse(status_code=400, content=record)

        try:
            prediction = model_predict(image)
        except Exception as error:  # Keep the API response useful without leaking details.
            LOGGER.exception("Inference failed for request %s", resolved_request_id)
            record = {
                **base_record,
                "status": "error",
                "action": "inference_unavailable",
                "prediction_called": True,
                "prediction": None,
                "error_type": type(error).__name__,
            }
            append_jsonl(record, trace_path)
            return JSONResponse(status_code=503, content=record)

        record = {
            **base_record,
            "prediction_called": True,
            "prediction": prediction,
        }
        append_jsonl(record, trace_path)
        return record

    return application


app = create_app()
