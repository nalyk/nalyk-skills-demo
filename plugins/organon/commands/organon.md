---
name: organon
description: "Philosophical reasoning engine — auto-detects whether you need a decision analysis or code review, selects depth, and applies the relevant principles from 20 philosophers."
---

# /organon — Auto-Detect Mode

Invoke the `organon` skill in auto-detect mode.

## Behavior

1. Read the current conversation context to determine the situation
2. Classify as **decision** (engineering choice, architecture, debugging) or **review** (code quality, design evaluation)
3. Auto-select depth:
   - **Quick**: Clear situation, single principle applies
   - **Standard**: Non-trivial, multiple principles or ambiguity
   - **Deep**: Architectural, irreversible, high-stakes — delegates to philosopher-council agent
4. Execute the organon skill with detected mode and depth

## Arguments

Optional depth override:
- `/organon quick` — Force quick depth (one principle + action)
- `/organon standard` — Force standard depth (multiple principles + protocol summary)
- `/organon deep` — Force deep depth (full 22-step protocol via philosopher-council agent)

Optional topic:
- `/organon <topic>` — Apply organon to a specific topic/question
- `/organon deep should we use microservices or monolith` — Deep analysis of a specific decision

## Examples

```
/organon
```
Auto-detects from conversation context.

```
/organon deep
```
Forces full 22-step philosophical analysis of current context.

```
/organon should we add caching here or optimize the query
```
Decision analysis on a specific question.
