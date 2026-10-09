# Lab 02 — Build a Repeatable Baseline

Today your team will build the smallest complete technical path for its project: load a small sample, check it, run a simple baseline, measure one result, and save that result.

The goal is not to find the best model. A simple or even weak result is acceptable. It must be real, repeatable, and honest about what it does not prove.

## Before class

There is nothing to submit before class. Start from the same team repository and project direction you created in Lab 01. The AIT Studio activity is private practice and does not create your team's Lab work.

## What you should have before leaving

Your team repository should contain these Lab 02 artifacts:

```text
README.md                         updated setup and run instructions
data/
  README.md                       data source and placement instructions
docs/
  split_strategy.md               evaluation or split decision
reports/
  baseline_metrics.json           result created by the pipeline
src/
  baseline_pipeline.py            runnable baseline
requirements.txt                  packages needed by the pipeline
```

You may use `notebooks/baseline_pipeline.ipynb` instead of the Python script. If you use a notebook, it must run from top to bottom without hidden manual steps and must still create `reports/baseline_metrics.json`.

## 1. Choose the smallest complete run — 10 minutes

Agree on:

- one small, documented data sample;
- one simple baseline;
- one primary metric;
- one clear limitation you already expect.

A **baseline** is the initial measured result from your first experiment. It gives your team a starting point for comparing later experiments. Use a simple AI model or a pretrained model without heavy tuning, and focus on completing the full path from data to a saved result.

A **metric** is the number used to summarise the experiment result. Use the metric that fits your project and save its value with the run.

Do not spend this Lab searching for the best model or tuning many settings. Keep each supporting document to a short paragraph or a few bullets. The five work sections use 85 minutes, leaving five minutes to recover from a setup problem or finish the final commit.

## 2. Prepare and document the data — 15 minutes

Create `data/README.md` and record:

- the dataset or sample name;
- its source, or how the team created it;
- any permission, licence, or access limit you know about, or `not yet confirmed`;
- the expected folder structure;
- whether the data is committed, downloaded, generated, or provided separately;
- any preparation needed before the run.

Do not commit passwords, private links, restricted personal data, or large datasets. If the data cannot be stored in Git, document how an authorised team member places it in the expected location.

## 3. Keep the evaluation separate — 15 minutes

Create `docs/split_strategy.md`.

A **held-out evaluation sample** is a small set of examples that you do not use to fit, choose, or adjust the baseline. It gives a more honest first result.

Use the branch that matches your baseline:

- **Model trained by your team:** state what is used for training and what is kept for evaluation. Explain whether the split is random, time-based, group-based, scene-based, or another suitable method.
- **Pretrained model used without additional training:** state that no training split is needed for this run. Describe the separate sample used for evaluation.

In both cases, explain:

- whether the evaluation resembles the examples the system may receive later; if it does not, say so as a limitation;
- one limitation of this first evaluation.

For example, consecutive frames from the same video should normally stay in the same group rather than being divided randomly between fitting and evaluation.

## 4. Run the baseline and save the result — 30 minutes

Create `src/baseline_pipeline.py` or the reproducible notebook. It should:

1. load the documented sample;
2. check the required files, columns, labels, or input shape;
3. create or load the evaluation split or held-out sample;
4. fit or apply the simple baseline;
5. calculate one primary metric;
6. write the result to `reports/baseline_metrics.json` automatically.

Use a small JSON record like this:

```json
{
  "experiment": "firewatch_baseline_v1",
  "data": "120 labelled fire and no-fire images",
  "evaluation": "30 images kept for evaluation",
  "model": "pretrained image classifier",
  "metric": {
    "name": "accuracy",
    "value": 0.73
  },
  "limitation": "small sample with few night images"
}
```

This example reports 73% accuracy on 30 evaluation images. The pipeline calculates the metric value. Your team supplies the short descriptions of the experiment, data, model, and limitation in the script. The script or notebook then writes both the text and the number to the JSON file automatically.

## 5. Document and rerun the baseline — 15 minutes

Now that the pipeline works, update the main `README.md` with:

- the Python version or environment you used;
- the install command;
- where to find the data instructions;
- the exact command that runs the baseline;
- the result file created by that command: `reports/baseline_metrics.json`.

List the packages needed by the pipeline in `requirements.txt`.

A **clean checkout** means that a teammate uses a fresh clone in a new folder or another clean environment, follows the written instructions, and runs the baseline without relying on an unmentioned path, file, or step from another person's computer. A normal pull inside the author's working folder is not this check because hidden local files may remain there.

Ask a teammate who did not write most of the pipeline to:

1. make a fresh clone or clean working copy and start at its repository root;
2. follow the `README.md` without verbal instructions from the author;
3. run the documented command;
4. confirm that `reports/baseline_metrics.json` is created or updated.

Fix any missing step, local-only path, dependency, or data instruction that the teammate finds. Then show me the run command, the saved result, and the limitation, and commit the Lab 02 work to the team repository.

## Lab 02 is complete when

- the README gives one runnable command and says that it creates `reports/baseline_metrics.json`;
- `data/README.md` explains how the sample is obtained and placed;
- `docs/split_strategy.md` explains the evaluation choice;
- the script or notebook completes the smallest data-to-metric path;
- `requirements.txt` lists any packages needed by the pipeline;
- the run creates `reports/baseline_metrics.json` automatically with a real measured value and an honest limitation;
- a teammate has followed the instructions and reproduced the run;
- the Lab 02 work is committed to the team repository.

One small, repeatable baseline is enough. You do not need a strong score, a large training run, a deployed service, or a polished application in this Lab.
