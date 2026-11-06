from __future__ import annotations

import unittest

from src.input_validation import combine_status, route_request


class InputValidationTests(unittest.TestCase):
    def test_error_overrides_warning(self) -> None:
        checks = [{"status": "warning"}, {"status": "error"}, {"status": "pass"}]
        self.assertEqual(combine_status(checks), "error")

    def test_warning_does_not_call_prediction(self) -> None:
        called = False

        def predict(_: dict[str, object]) -> dict[str, object]:
            nonlocal called
            called = True
            return {}

        validation = {"request_id": "req-warning", "status": "warning", "action": "route_for_review"}
        result = route_request({}, validation, predict)
        self.assertFalse(called)
        self.assertFalse(result["prediction_called"])

    def test_pass_calls_prediction(self) -> None:
        validation = {"request_id": "req-pass", "status": "pass", "action": "continue_to_prediction"}
        result = route_request({}, validation, lambda _: {"label": "ok"})
        self.assertTrue(result["prediction_called"])
        self.assertEqual(result["prediction"], {"label": "ok"})


if __name__ == "__main__":
    unittest.main()
