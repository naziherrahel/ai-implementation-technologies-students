# Lab 01 — Choose a Project We Can Actually Build

Today your team will choose one realistic project direction and create a small repository foundation for the semester.

You are not training a model today. Start with a person and a useful change, not a favourite model. AI should have a sensible role, but it will be only one part of the future system.

## Before class

There is nothing to submit before class. The AIT Studio activity is private practice and does not create your team's Lab work.

## What you should have before leaving

Your team repository should contain only two required documents:

```text
README.md
docs/
  project_brief.md
```

The repository can contain normal setup files such as `.gitignore`, but do not create extra reports, diagrams, model files, or datasets for this Lab.

## 1. Form your team and compare directions — 15 minutes

Work in a team of three or four unless we have agreed on another size.

Discuss possible directions aloud. Do not write several complete proposals. Look for a situation where:

- a real person or group needs something to improve;
- the input (what the system receives) and useful result (what it should produce) can be described clearly;
- the system may need to learn a pattern from examples instead of relying only on fixed `if/then` rules;
- your team can realistically access some relevant data, even if it is only a small but realistic sample at first.

## 2. Choose one direction — 20 minutes

Choose one main direction that your team can explain. Keep a backup only if access to the first data source is uncertain.

Before creating documents, explain the direction to each other:

- Who needs the system?
- What situation should change?
- What will enter the future system?
- What useful output should come out?
- What action or decision follows that output?
- Why might AI help, and what else belongs to the system besides the model?

If the direction still begins with a model name, rewrite it around the user and useful change.

## 3. Create the repository and project brief — 40 minutes

Create one team repository that you will continue using throughout the course.

In `README.md`, include:

- team name;
- team members;
- where the team will communicate, such as a Telegram group or another agreed space;
- one-sentence project direction — who you want to help, what the system will use, and what useful change it should support.

For example: “We want to help campus facilities staff use bin images to identify bins that may need collection.” This describes the project without claiming that the system already exists or naming a favourite model.

Create `docs/project_brief.md` using this structure:

```markdown
# Project brief

## User and situation
Who needs the system? What happens now, and what should become better?

## What the system should do
- Input:
- Useful output:
- Action or decision after the output:

## Why AI may help
What pattern may need to be learned? What rules, interface, people, or review steps also belong to the system?

## Initial data plan
- Where the data may come from:
- What we can access now:
- What still needs confirmation:

## Three next actions
1.
2.
3.
```

Under **What still needs confirmation**, record only open questions that matter before the team can proceed. For example: whether you can obtain suitable data, whether you are allowed to use it, or whether the project direction is small enough for this course. You do not need to answer every question today.

The three next actions are small steps that help the team answer those questions and move forward. They are written inside the project brief, not as three extra documents or repository issues. Examples include confirming access to a small realistic sample, checking its format, or making sure every team member can open the repository.

## 4. Show, revise, and commit — 15 minutes

Before you leave, show me the README and project brief. Be ready to explain:

- the user and useful change;
- the input, output, and next action;
- why AI has a sensible role;
- where the first data may come from;
- what still needs confirmation and what the team will do next.

If one part is unclear, make the requested revision. Then commit the Lab 01 documents to the team repository.

## Lab 01 is complete when

- another person can understand the project direction from `README.md`;
- `docs/project_brief.md` answers the prompts above without pretending that uncertain facts are confirmed;
- the open questions and three next actions are specific to your project;
- every team member can open the repository.

One clear, feasible direction is enough. Do not train, evaluate, deploy, or monitor a model in Lab 01.
