# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
========================================
Owner: Alex
Pets: Rex, Whiskers
Available time: 60 minutes
----------------------------------------
1. Morning walk (30 min, priority: high, pending)
2. Feed breakfast (10 min, priority: high, done)
3. Brush fur (15 min, priority: medium, pending)
----------------------------------------
Total scheduled time: 55 minutes
========================================

Scheduling conflicts:
- Conflict: 'Brush fur' and 'Play with laser pointer' are both scheduled at 09:00.
```

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover:

- Task completion
- Adding tasks to a pet
- Sorting tasks by time
- Recurring task behavior
- Conflict detection
- Empty scheduler edge case

Sample test output:

```
# Paste your pytest output here
```

### Confidence level: ⭐⭐⭐⭐☆ (4/5)

The system is reliable for all the behaviors covered above — sorting, filtering, recurrence, and the empty-scheduler edge case all pass consistently. The one point held back is conflict detection: it currently only flags tasks that share an exact `scheduled_time` match, so it won't catch overlapping-duration conflicts (e.g., a 30-minute task starting at 08:00 overlapping one that starts at 08:15). That's a reasonable next improvement rather than a current defect.

## 📐 Smarter Scheduling

- **Sorting** — `Scheduler.sort_by_time()` returns all tasks ordered by `scheduled_time`, earliest first, so an owner can see their day laid out chronologically instead of in whatever order tasks were added.
- **Filtering** — `Scheduler.filter_by_pet()` narrows the task list down to a single pet's tasks, and `Scheduler.filter_by_status()` splits tasks into completed vs. pending, so an owner can quickly answer "what's left to do for Rex today?"
- **Recurring tasks** — `Task.create_next_occurrence()` generates the next copy of a recurring task (1 day later for `"daily"`, 7 days later for `"weekly"`), so completing a repeating chore like medication or grooming automatically rolls it forward instead of it disappearing.
- **Conflict detection** — `Scheduler.find_conflicts()` scans all tasks and flags any pair scheduled at the exact same `scheduled_time`, returning a readable warning instead of crashing or silently double-booking. This is an exact-time check for now, not a full overlapping-duration check.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by `scheduled_time`, earliest first |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Filter by pet name or completion status |
| Recurring tasks | `Task.create_next_occurrence()` | Daily tasks recur +1 day, weekly tasks recur +7 days |
| Conflict handling | `Scheduler.find_conflicts()` | Warns when two tasks share the same exact `scheduled_time` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->


**SystemDesign**



