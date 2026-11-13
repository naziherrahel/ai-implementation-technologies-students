# Lab 06 — Put a Real AI Service on a Cloud VM

In this practice, we will deploy a small image-detection API to an Ubuntu virtual machine in Yandex Cloud. The example uses the pretrained `yolo26n.pt` nano model on CPU. Use it to learn the deployment path; its detections are not evaluation evidence for your project.

Follow the reference deployment with me, then apply the same path to your team project.

## By the end of the practice

- You can connect to the VM with SSH.
- `GET /health` identifies the running service and model.
- `POST /predict` accepts a JPEG or PNG image.
- Invalid input stops before inference.
- Valid input reaches the pretrained YOLO model.
- Each request leaves a JSONL record on the VM.

## Before creating the VM: check the cost

Do not assume that linking a bank card gives you a free trial. Some eligible individual accounts may receive a start grant of 4,000 ₽, while other new accounts begin with paid consumption. Your own **Billing** page shows which case applies to you.

Open **Billing** and check what your own account shows before creating resources:

- the grant amount, if any;
- its expiry date;
- whether the account is already using paid consumption.

Do not assume a 60-day free period. If your Billing page shows no grant, do not start paid resources unless you have decided to accept the cost. You can still follow the demonstration and run the service locally. Stop or delete unused resources when the Lab ends.

Official information: [Yandex Cloud offers](https://yandex.cloud/ru/all-offers) and [billing registration](https://yandex.cloud/en/docs/billing/quickstart/).

## 1. Prepare an SSH key

First check whether this computer already has an Ed25519 public key.

macOS or Linux:

```bash
test -f ~/.ssh/id_ed25519.pub && echo "public key found"
```

Windows PowerShell:

```powershell
Test-Path $env:USERPROFILE\.ssh\id_ed25519.pub
```

If the command reports an existing key and you know how to use its matching private key, you may reuse it. Do not overwrite an existing key. Otherwise, create a new pair in Terminal on macOS or Linux, or PowerShell on Windows:

```text
ssh-keygen -t ed25519 -C "ait-cloud-practice"
```

Press Enter to accept the suggested location. When asked for a passphrase, choose one you can remember.

If `ssh-keygen` says that `id_ed25519` already exists, answer `n`. Do not overwrite it. Use the existing public key or ask for help choosing a different filename.

Copy the **public** key. Never upload or share the private key.

macOS or Linux:

```bash
cat ~/.ssh/id_ed25519.pub
```

Windows PowerShell:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

## 2. Create the Ubuntu VM

In Yandex Cloud, create one Compute Cloud VM with:

- Ubuntu 24.04 LTS;
- network SSD boot disk;
- 10 GB boot-disk minimum, or 20 GB if your quota allows it;
- 2 vCPU;
- 4 GB RAM;
- a public IPv4 address;
- your public SSH key.

Choose the custom configuration rather than a larger CPU preset. A 10 GB disk is enough for this starter. Choose 20 GB when your quota allows it, especially if the VM will also hold your team project. Use 2 vCPU and 4 GB RAM for this practice. Four vCPU may be faster, but it is not necessary; do not choose 8 vCPU for this task.

In the **Access** or **SSH key** section, enter the VM username and paste the single line copied from `id_ed25519.pub`. Do not paste `id_ed25519`, and do not upload the private key.

Record the VM username and public IP before continuing.

Yandex reference: [Create a Linux VM](https://yandex.cloud/en/docs/compute/quickstart/quick-create-linux).

## 3. Connect with SSH

The same command works in macOS Terminal, Linux Terminal, and current Windows PowerShell:

```text
ssh <username>@<public-ip>
```

Accept the host fingerprint only after checking that the IP matches your VM. A successful connection gives you a shell on Ubuntu.

Yandex reference: [Connect to a VM over SSH](https://yandex.cloud/en/docs/compute/operations/vm-connect/ssh).

## 4. Copy the reference service to the VM

Leave the SSH session open. Open a second terminal on your own computer, move to this practice directory, and copy the `starter` folder:

```text
scp -r starter <username>@<public-ip>:~/
```

This `scp` command works on macOS, Linux, and current Windows PowerShell. Return to the SSH window. From this point onward, all commands run inside the Ubuntu VM.

```bash
mv ~/starter ~/ait-yolo-service
cd ~/ait-yolo-service
```

## 5. Prepare Python on the VM

```bash
sudo apt update
sudo apt install -y python3-venv libgl1
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r requirements.txt
cp .env.example .env
python3 -m unittest tests/test_app.py
```

These tests check input routing and evidence generation without downloading the real model. The first installation downloads several hundred megabytes and may take 5–10 minutes on the classroom network. Continue only after the terminal returns to the prompt and the tests report `OK`.

## 6. Start the service

```bash
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000
```

`0.0.0.0` allows the service to receive requests through the VM network interface.

Keep this terminal open while the service is running.

## 7. Send a real image through the model

Open these pages in your browser:

- `http://<public-ip>:8000/health`
- `http://<public-ip>:8000/docs`

This classroom endpoint uses HTTP. Upload only the provided example or another non-sensitive test image.

Before the first valid prediction, `/health` shows `"model_loaded": false`. This is expected: the starter loads the model only when it receives the first valid image. After that prediction, the value becomes `true`.

For a repeatable example, download the [Ultralytics bus image](https://ultralytics.com/images/bus.jpg) to your computer.

In `/docs`:

1. Open `POST /predict` and select **Try it out**.
2. Enter `req-cloud-001` as the request ID.
3. Upload `bus.jpg`.
4. Select **Execute**.

The first valid request is slower because the VM downloads `yolo26n.pt` before running CPU inference. The response should show detected objects, confidence values, bounding-box coordinates, and inference time. These are pretrained general-purpose detections; they are not project evaluation results.

When reading the response:

- `confidence_threshold: 0.25` means detections below that model score are omitted;
- `latency_ms` measures the model prediction call on the VM, not the complete browser-to-server time;
- `box_xyxy` gives the left, top, right, and bottom coordinates of the detected object in pixels.

A confidence score is not proof that a detection is correct.

Ultralytics reference: [Predict mode](https://docs.ultralytics.com/modes/predict/).

## 8. Check that invalid input does not reach the model

Send a text file through the same endpoint. The response should have:

```json
{
  "status": "error",
  "action": "reject_input",
  "prediction_called": false
}
```

The complete response also shows which executable checks failed.

The browser will show HTTP status `400` for this request. That is the expected result for input that the service rejects.

## 9. Inspect the generated evidence

Return to the SSH window. Stop the server with `Ctrl+C`, then run:

```bash
tail -n 2 reports/yolo_predictions.jsonl
```

The two lines should connect each request with its decoded image properties, validation checks, routing action, and prediction result. Focus on four fields:

- `status` and `action`: what the service decided;
- `checks`: which input rules passed or failed;
- `prediction_called`: whether the model ran;
- `prediction`: the detections, or `null` when the input was rejected.

## Team project task

Now deploy the inference path that your team developed in Labs 04–05.

1. Add a small API endpoint for the input your project actually uses.
2. Keep your executable input checks before prediction.
3. Call your existing model or baseline only after the input passes.
4. Record the request, validation result, action, and prediction in JSONL.
5. Run the service on the team VM.
6. Demonstrate one valid request and one rejected request.

Use the reference service to understand the connection between the API, validation, model, and evidence. Do not copy its image rules if your project uses another input type.

Before leaving, make sure another team member can start the service from the commands in your repository README. Commit the working code and one small, non-sensitive example trace.

## Completion check

Lab 06 is complete when another computer can call your team service, one valid request reaches prediction, one invalid request stops before prediction, and the JSONL trace contains both decisions.

## If something does not work

| Symptom | Check |
|---|---|
| SSH times out | The VM is running and the public IP is correct |
| `Permission denied (publickey)` | VM username and the public key attached to the VM |
| `/docs` does not open | The public IP, the Uvicorn command, and whether the service is still running |
| First prediction fails | VM internet access, free disk space, and the model-download message in the terminal |
| Process stops during installation or inference | VM RAM and disk; use the recommended configuration |

## Finish safely

Do not commit `.env`, SSH keys, cloud credentials, private images, or access tokens. When the practice is complete, stop the service. Stop or delete the VM if the team will not continue using it.
