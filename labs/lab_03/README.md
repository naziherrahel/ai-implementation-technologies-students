# Lab 03 — Decide What Counts as Acceptable

Today your team will decide what the system must do, which failure matters most, and how you will judge later results.

Write your Lab 03 work in `docs/project_decisions.md`. You will not change the model or design the architecture today.

## Before class

There is nothing to submit before class. Start from the same team repository used in Labs 01–02 and make sure you can open:

- `docs/project_brief.md`;
- `docs/split_strategy.md`;
- `reports/baseline_metrics.json`.

The AIT Studio activity is private practice. It does not create your team's Lab work.

## 1. Check the project direction — 10 minutes

Read the three existing files together. You are not choosing a new project. Decide whether the baseline gives you a reason to:

- **continue** with the current direction;
- **simplify** what the system will do; or
- **narrow** the user, input, output, or operating conditions.

Create `docs/project_decisions.md` and begin with:

```markdown
# Project decisions

## Lab 03 — Acceptance

### Decision after the baseline
Decision: Continue / Simplify / Narrow
Reason: Based on [measured result] and [important limitation], we decided to...
```

A weak result does not automatically end the project.

## 2. Describe the required behavior — 15 minutes

Add this section:

```markdown
### Required behavior
- Normal input:
- Invalid input:
- Valid input with an uncertain result:

### One quality that matters
-
```

Lab 01 already describes the user, input, useful output, and next action. Do not rewrite that project description. Add what the system returns for each input state and what the user can do next. A **fallback** is what happens when the normal path cannot give a reliable result. For example, the system might reject an invalid input with a reason or send an uncertain result for human review.

Choose one relevant quality besides the model result, such as response time, reliability, privacy, or usability. If you cannot choose a number yet, write what you would need to measure first.

## 3. Define one acceptance check — 25 minutes

Choose the failure that matters most to the user and add:

```markdown
### One acceptance check
- Important failure:
- Metric that would show this failure:
- Preliminary acceptance threshold:
- Where will we check it?
- Why this number for now?
- Evidence still missing:
```

Use the Lab 02 metric if it directly shows this failure. Otherwise, name the additional metric a later evaluation will need. A **preliminary acceptance threshold** is a proposed limit for that later evaluation. Your baseline does not need to meet this limit today, and the proposed number does not prove that the system is ready.

If your team has no evidence for a number yet, write `not set yet` and state what evidence would help you choose it. Do not invent a threshold only to complete the field.

FireWatch example:

```text
Failure: a fire is missed at night
Metric: false-negative rate on night images
Starting threshold: below 10% for a later evaluation
Missing evidence: more labelled night images
```

The value is illustrative. Choose a limit that makes sense for your project.

**Only if relevant:** a model-score cutoff changes one prediction, while an acceptance threshold judges results across an evaluation sample. For a response-time target, state what is timed and on which device.

## 4. Add three short failure cases — 20 minutes

Add one case from each area below. Use short phrases rather than paragraphs.

```markdown
### Failure cases

| Area | What could go wrong and why it matters | How would we notice it? | Planned response |
| --- | --- | --- | --- |
| Data or input | | | |
| Model behavior | | | |
| Integration or workflow | | | |
```

One failure case must match the important failure in your acceptance check. “The AI fails” is too general. Name a situation that could actually happen in your project and something observable that would reveal it.

Write the response you would want. You will implement it in a later Lab.

## 5. Review, show, and commit — 15 minutes

Ask a teammate to choose one required behavior or fallback and find its matching failure, metric, proposed threshold, and missing evidence. If the connection is unclear, fix the relevant section.

Then show me the file and explain the baseline decision, the normal path and fallbacks, and the acceptance check with its matching failure case.

Commit the Lab 03 work to the team repository.

## Lab 03 is complete when

- `docs/project_decisions.md` contains the Lab 03 acceptance section;
- the measured baseline result is clearly separated from the proposed threshold;
- one connected chain can be followed from required behavior to missing evidence;
- the file contains three short, project-specific failure cases.

Keep this file. You will add later project decisions to it in the next Labs.
