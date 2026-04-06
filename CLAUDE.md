# Agent Rules

## 1. Docs First
Before any implementation or decision, review the relevant documentation in `docs/`.
Use `docs/` for architecture, design philosophy, and product-level references.

**Important:** Files under `docs/specs/` are read-only generated mirrors.
Do not edit files under `docs/specs/` directly.
The source of truth for feature specs is `.kiro/specs/`.

## 2. Spec Updates
If a feature spec must be updated, edit the corresponding files in `.kiro/specs/`.
After implementation, make sure the relevant `.kiro/specs/` files reflect the final state.
Changes to `.kiro/specs/` are automatically mirrored to `docs/specs/` via a sync hook.

## 3. Plan First
Do not start coding immediately.
Always create a clear plan first.

The plan must include:
- Understanding of the task
- Relevant references from `docs/` and `.kiro/specs/`
- Step-by-step implementation approach

## 4. Then Execute
Only after the plan is defined, proceed with implementation.

## 5. No Assumptions
Do not guess specifications.
If something is unclear or missing, explicitly state it.