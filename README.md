# PawPal+

**PawPal+** is a pet care planning assistant. It helps a pet owner track care tasks (walks, feeding, meds, grooming, enrichment) across one or more pets, build a schedule from those tasks, and catch scheduling problems before they happen. The core scheduling logic is implemented in plain Python and is exposed through both a CLI demo and a Streamlit web UI.

## Features

- Add pets and care tasks (title, duration, priority, scheduled time, recurrence)
- Sort tasks by scheduled time
- Filter tasks by pet
- Filter tasks by completion status (done vs. pending)
- Generate recurring task examples (daily/weekly roll-forward)
- Detect exact-time scheduling conflicts
- View results in both a CLI demo and a Streamlit UI

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the CLI demo

```bash
python main.py
```

### Run the Streamlit app

```bash
streamlit run app.py
```

## Demo Walkthrough

The Streamlit UI (`app.py`) is organized into two sections: **Owner & Pet** and **Build Schedule**.

**Owner & Pet** lets you enter the owner's name, the pet's name, and species, then add care tasks one at a time — each with a title, duration, priority, scheduled time (`HH:MM`), recurrence (`none`/`daily`/`weekly`), and a completed checkbox. Added tasks appear in a running table.

**Build Schedule** takes the saved tasks and runs them through the `Scheduler` backend, then displays:
- All tasks sorted by scheduled time
- Pending tasks
- Completed tasks
- Any scheduling conflicts (two tasks with the same exact time)

**Example workflow:**

```
Add owner → add pet → add tasks → generate schedule → view sorted tasks and conflict warnings
```

1. Enter an owner name (e.g. "Jordan") and a pet name (e.g. "Mochi").
2. Add a few tasks — e.g. "Morning walk" at 08:00 (high priority), "Feed breakfast" at 07:00 (high priority, mark completed), "Brush fur" at 09:00 (medium priority, daily recurrence).
3. Click **Generate schedule**.
4. Review the time-sorted schedule, the pending/completed breakdown, and any conflict warnings (e.g. two tasks both scheduled at 09:00).

## Scheduler Behaviors

| Feature | Method | Notes |
|---------|--------|-------|
| Sorting | `Scheduler.sort_by_time()` | Returns all tasks ordered by `scheduled_time`, earliest first |
| Filter by pet | `Scheduler.filter_by_pet(pet_name)` | Returns only the tasks belonging to a given pet |
| Filter by status | `Scheduler.filter_by_status(completed)` | Returns only tasks matching a completion state (done/pending) |
| Conflict detection | `Scheduler.find_conflicts()` | Flags any pair of tasks sharing the exact same `scheduled_time` |
| Recurring tasks | `Task.create_next_occurrence()` / `Scheduler.expand_recurring_tasks()` | Daily tasks recur +1 day, weekly tasks recur +7 days |

**Note:** conflict detection is an exact-time match, not a full overlapping-duration check — a 30-minute task starting at 08:00 won't be flagged against one starting at 08:15.

## CLI Sample Output

```
Original task list:
- 08:00: Morning walk (30 min, priority: high, pending)
- 07:00: Feed breakfast (10 min, priority: high, done)
- 09:00: Brush fur (15 min, priority: medium, pending)
- 09:00: Play with laser pointer (20 min, priority: low, pending)
========================================
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

Tasks sorted by time:
- 07:00: Feed breakfast (10 min, priority: high, done)
- 08:00: Morning walk (30 min, priority: high, pending)
- 09:00: Brush fur (15 min, priority: medium, pending)
- 09:00: Play with laser pointer (20 min, priority: low, pending)

Tasks for Rex:
- Morning walk (30 min, priority: high, pending)
- Feed breakfast (10 min, priority: high, done)

Completed tasks:
- Feed breakfast (10 min, priority: high, done)

Pending tasks:
- Morning walk (30 min, priority: high, pending)
- Brush fur (15 min, priority: medium, pending)
- Play with laser pointer (20 min, priority: low, pending)

Upcoming recurring task copies:
- Morning walk (+1d) (30 min, priority: high, pending)
- Morning walk (+2d) (30 min, priority: high, pending)
- Morning walk (+3d) (30 min, priority: high, pending)
- Brush fur (+7d) (15 min, priority: medium, pending)

Scheduling conflicts:
- Conflict: 'Brush fur' and 'Play with laser pointer' are both scheduled at 09:00.

Recurring task demo:
- Created: Give medication (5 min, priority: high, pending) (due 2026-07-05)
- Completed: Give medication (5 min, priority: high, done) (due 2026-07-05)
- Next occurrence: Give medication (5 min, priority: high, pending) (due 2026-07-06)
```

## Testing

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover:

- Task completion (`mark_complete`)
- Adding a task to a pet
- Sorting tasks by time
- Recurring task logic (daily roll-forward)
- Conflict detection
- Empty scheduler edge case

Sample test output:

```
============================= test session starts ==============================
collected 6 items

tests/test_pawpal.py::test_task_completion PASSED                        [ 16%]
tests/test_pawpal.py::test_task_addition PASSED                          [ 33%]
tests/test_pawpal.py::test_sorting_correctness PASSED                    [ 50%]
tests/test_pawpal.py::test_recurrence_logic PASSED                       [ 66%]
tests/test_pawpal.py::test_conflict_detection PASSED                     [ 83%]
tests/test_pawpal.py::test_empty_task_list PASSED                        [100%]

============================== 6 passed in 0.02s ===============================
```
