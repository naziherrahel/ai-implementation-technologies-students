from __future__ import annotations

import json
from io import BytesIO
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from app import create_app


class CloudDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.trace_path = Path(self.temp_dir.name) / "trace.jsonl"
        self.predict_calls = 0

        def fake_predict(_: Image.Image):
            self.predict_calls += 1
            return {
                "model": "fake-nano.pt",
                "confidence_threshold": 0.25,
                "latency_ms": 1.0,
                "object_count": 1,
                "detections": [
                    {
                        "class_id": 0,
                        "class_name": "person",
                        "confidence": 0.9,
                        "box_xyxy": [1.0, 2.0, 30.0, 40.0],
                    }
                ],
            }

        self.client = TestClient(create_app(self.trace_path, fake_predict))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @staticmethod
    def image_bytes(width: int = 320, height: int = 240) -> bytes:
        buffer = BytesIO()
        Image.new("RGB", (width, height), color=(40, 80, 120)).save(
            buffer,
            format="JPEG",
        )
        return buffer.getvalue()

    def request(
        self,
        request_id: str = "req-test",
        data: bytes | None = None,
        filename: str = "sample.jpg",
        content_type: str = "image/jpeg",
    ):
        return self.client.post(
            "/predict",
            data={"request_id": request_id},
            files={"file": (filename, data or self.image_bytes(), content_type)},
        )

    def test_pass_calls_prediction(self) -> None:
        response = self.request()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "pass")
        self.assertTrue(response.json()["prediction_called"])
        self.assertEqual(response.json()["prediction"]["object_count"], 1)
        self.assertEqual(self.predict_calls, 1)

    def test_invalid_upload_stops_before_prediction(self) -> None:
        response = self.request(
            request_id="req-invalid",
            data=b"not an image",
            filename="notes.txt",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")
        self.assertFalse(response.json()["prediction_called"])
        self.assertEqual(self.predict_calls, 0)

    def test_each_request_leaves_one_trace_record(self) -> None:
        self.request(request_id="req-trace")
        records = [json.loads(line) for line in self.trace_path.read_text().splitlines()]
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["request_id"], "req-trace")
        self.assertEqual(records[0]["image"]["width"], 320)


if __name__ == "__main__":
    unittest.main()
