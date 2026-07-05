from datetime import date

from pawpal_system import Pet, Scheduler, Task


def test_task_completion():
    task = Task("Morning walk", 20, "high")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    pet = Pet("Mochi", "dog")
    task = Task("Feed dinner", 10, "medium")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_sorting_correctness():
    task_a = Task("Brush fur", 15, "medium", scheduled_time="09:00")
    task_b = Task("Feed breakfast", 10, "high", scheduled_time="07:00")
    task_c = Task("Morning walk", 30, "high", scheduled_time="08:00")

    scheduler = Scheduler(tasks=[task_a, task_b, task_c])
    sorted_tasks = scheduler.sort_by_time()

    assert [task.scheduled_time for task in sorted_tasks] == ["07:00", "08:00", "09:00"]


def test_recurrence_logic():
    daily_task = Task(
        "Give medication",
        5,
        "high",
        scheduled_time="08:30",
        pet_name="Rex",
        recurrence="daily",
        due_date=date(2026, 7, 5),
    )

    daily_task.mark_complete()
    next_task = daily_task.create_next_occurrence()

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 6)
    assert next_task.completed is False


def test_conflict_detection():
    task_a = Task("Brush fur", 15, "medium", scheduled_time="09:00", pet_name="Whiskers")
    task_b = Task("Play with laser pointer", 20, "low", scheduled_time="09:00", pet_name="Whiskers")

    scheduler = Scheduler(tasks=[task_a, task_b])
    conflicts = scheduler.find_conflicts()

    assert len(conflicts) >= 1


def test_empty_task_list():
    scheduler = Scheduler(tasks=[])

    assert scheduler.sort_by_time() == []
    assert scheduler.find_conflicts() == []
