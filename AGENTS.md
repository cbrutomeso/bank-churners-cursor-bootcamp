# AGENTS.md

## Purpose

This file defines how AI agents should operate in this repository.

The goal is to ensure consistent, structured, and high-quality outputs across all tasks:
EDA, modeling, application development, and reporting.

---

## Standard Workflow

For any non-trivial task, follow this sequence:

1. Understand context

   * Read `README.md`
   * Read `docs/03_success_criteria.md`
   * Read the relevant task file in `docs/`

2. Plan

   * Propose a clear step-by-step plan (5–8 steps)
   * Do NOT write code yet

3. Execute

   * Implement the solution step by step
   * Keep changes modular and readable
   * Avoid large, unstructured edits

4. Validate

   * Ensure code runs end-to-end
   * Check assumptions explicitly
   * Verify outputs against success criteria

5. Summarize

   * What was done
   * What remains
   * Risks or limitations

---

## Directory Rules

* Always follow the project structure defined in `README.md`
* Reuse existing directories
* Do NOT create new top-level folders unless explicitly required

---

## Development Principles

* Prefer simple and interpretable solutions first
* Avoid unnecessary complexity
* Keep outputs understandable for a human reviewer
* When unsure, propose alternatives with tradeoffs

---

## Data Reasoning Guidelines

* Correlation does NOT imply causation
* Always consider potential data leakage
* Be explicit about assumptions
* Do not overstate conclusions

---

## Code Guidelines

* Keep functions small and readable
* Avoid duplication
* Do not hardcode paths
* Use existing project structure
* Write code that can be reused from `src/`

---

## Notebooks vs Code

* Notebooks are for exploration only
* Reusable logic must be moved to `src/`
* Avoid duplicating logic across notebooks and scripts

---

## Modeling Guidelines

* Always start with a baseline model
* Compare models fairly
* Use proper data splits (train/validation/test)
* Evaluate on holdout data only
* Mention limitations and risks

---

## Outputs

* Models must be saved in `artifacts/models/`
* Predictions must be saved in `artifacts/predictions/`
* Logs must be saved in `artifacts/logs/`
* Figures and tables must be saved in `reports/`

---

## Error Handling

* Do not silently ignore errors
* If something fails:

  * explain why
  * propose a fix
* Fail gracefully when possible

---

## When Unsure

* Ask for clarification OR
* Propose 2–3 reasonable approaches with pros/cons

---

## Anti-Patterns to Avoid

* Mixing exploration and production code
* Creating unnecessary folders
* Rewriting existing logic without reason
* Making assumptions without stating them
* Producing outputs without validation

---

## Definition of Done

A task is complete only if:

* It runs without errors
* It follows the required structure
* Outputs are generated in the correct locations
* Assumptions are documented
* Limitations are clearly stated
* It satisfies `docs/03_success_criteria.md`

---

## Environment & Dependencies

When required:

- Create or update `requirements.txt` with all necessary dependencies
- Pin every dependency to an exact version using `==`
- Ensure dependencies are minimal and relevant to the project
- Do not include unnecessary libraries
- Create the project virtual environment if it does not exist yet before running project code
- Treat the initial `requirements.txt` as a starter file, not a fixed contract
- Update `requirements.txt` whenever a task adds, removes, or changes dependencies
- By the end of the project, keep only the libraries that are actually used, each with an exact version

If environment variables are needed:

- Use a `.env` file
- Provide a `.env.example` with placeholders
- Do NOT hardcode secrets or environment-specific values

General rules:

- Code must run with the declared dependencies
- If you add or update a library, mention the exact version in the setup instructions or relevant documentation
- Avoid implicit or undocumented requirements