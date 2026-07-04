from pawpal_system import Pet, Task


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
