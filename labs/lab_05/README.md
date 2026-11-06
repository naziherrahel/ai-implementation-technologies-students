# Lab 05 — Executable Input Assurance

Your team will extend the Lab 04 inference demo with an input contract and a validator that decides what happens before prediction.

## Result to produce

```text
config/input_contract.json
src/input_validation.py
src/inference_demo.py
reports/validation_demo.jsonl
tests/test_input_validation.py
```

The JSONL trace is the evidence for the Lab. It should explain which rules ran, what each rule observed, the combined status, the chosen action, and whether prediction ran.

## Try the FireWatch starter

Open a terminal in the `starter` directory and run the same commands shown in the lecture:

```bash
python3 src/inference_demo.py
python3 -m unittest tests/test_input_validation.py
```

The first command should print one `pass`, one `error`, and one `warning`, then create `reports/validation_demo.jsonl`. The test command should run three tests successfully. The passing case calls `project_predict_stub()`; it does not run a trained model.

This FireWatch demo shows the validation path. After trying it, keep the working prediction function from Lab 04 and adapt the validator, contract, cases, and actions to your own project. Do not replace a working project prediction with the FireWatch stub.

## What the starter checks

The starter validates values supplied in the request (`input_ref`, format, width, height, and source) and compares the runtime transform identity with the contract. These are request-level checks.

It does not open the referenced file, prove that it exists, decode the bytes, inspect the decoded array, or verify the final model tensor. For example, `input_reference_present` means that the field is non-empty; it does not mean that the file was found. Keep the Lab claim at this level. If your existing project already measures a property from decoded data, you may use that measured value, but you do not need to build a decoder for this Lab.

## Decision used in this Lab

- `pass`: call `project_predict()`;
- `warning`: do not call prediction automatically; return `route_for_review`;
- `error`: do not call prediction; return `reject_input`.

When several rules fail, use the most severe result:

```text
error > warning > pass
```

## 1. Adapt three rules — 15 minutes

Copy these files into the matching locations in your team repository:

```text
starter/config/input_contract.json       → config/input_contract.json
starter/src/input_validation.py          → src/input_validation.py
starter/tests/test_input_validation.py   → tests/test_input_validation.py
```

Use `starter/src/inference_demo.py` as the integration example. Keep the working prediction function from your Lab 04 demo.

Adapt the contract and keep only rules that protect a real assumption in your project.

Include:

- one structural rule, such as a required field, format, dimensions, or value range;
- one project-specific rule, such as an approved source, unit, category, or timestamp condition;
- one warning rule tied to a meaningful review case.

The FireWatch starter uses `320 × 240` to make the demonstration easy to inspect. It is not a universal model limit. For your project, keep a threshold only when you can connect it to an interface requirement, evaluation result, or operating rule.

Give the deterministic preprocessing used by the demo one runtime identifier, and define it beside the inference code rather than accepting it from the incoming request. If your project already has a model package or manifest, load the identifier from there. Otherwise, use a clear local label such as `preprocessing-v1` and add a code comment naming the preprocessing it represents. Random training augmentation is separate and must not run during prediction.

## 2. Complete the validator — 25 minutes

Adapt `starter/src/input_validation.py` to your contract. Every evaluated check should produce:

```json
{
  "rule": "source_declared",
  "observed": "camera-c",
  "status": "warning",
  "action": "route_for_review"
}
```

Combine the check results into one overall status and action. An error must override a warning.

## 3. Connect the decision to inference — 20 minutes

Run validation before the existing `project_predict()` in `src/inference_demo.py`. You may paste your Lab 04 prediction function into the starter example or import it from your existing code.

The starter passes the complete request dictionary to the prediction callback. If your Lab 04 function accepts only an input reference, connect it with this small wrapper:

```python
def predict_from_request(request):
    return project_predict(request["input_ref"])
```

Pass `predict_from_request` to `route_request()` instead of the FireWatch stub.

- A passing request reaches prediction.
- A warning request produces review evidence but does not call prediction automatically.
- An error request stops before prediction.

Keep one `request_id` on the combined trace record so the validation decision and prediction outcome belong to the same attempt.

## 4. Run three cases and the tests — 20 minutes

Run one case for each status:

1. a normal input that passes;
2. an invalid input that produces an error;
3. a readable but unsupported input that produces a warning.

Use `src/inference_demo.py` to generate `reports/validation_demo.jsonl`. The supplied `project_predict_stub()` only proves whether the prediction function was called; it is not a model inference result. Then run:

```bash
python3 -m unittest tests/test_input_validation.py
```

The tests should prove that an error overrides a warning, a warning does not call prediction automatically, and a pass does call prediction.

## 5. Check the path and commit — 10 minutes

Ask a teammate to run the demo and answer:

- Which request reached prediction?
- Why did the warning request stop?
- Which checks produced an error, and how did severity precedence make the overall status `error`?
- Which fields connect the validation decision to the generated trace?

Commit the working validator, tests, contract, and generated JSONL trace.

## Completion check

Lab 05 is complete when one command produces pass, warning, and error records; only the passing request reaches prediction; the tests pass; and the generated trace explains every decision.
