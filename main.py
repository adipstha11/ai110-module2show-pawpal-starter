"""Simple CLI demo for PawPal+.

Creates an owner with a couple of pets, gives them some tasks,
runs the Scheduler, and prints out a clean "Today's Schedule" view.
"""

from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # First, let's create an owner
    owner = Owner("Alex", preferences="Prefers morning walks")

    # Now let's give them a couple of pets to look after
    dog = Pet("Rex", "Dog")
    cat = Pet("Whiskers", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Next, we'll set up a few tasks with different titles, durations, priorities, and times.
    # These are added out of time order on purpose, so we can show off sort_by_time() later.
    walk_task = Task("Morning walk", 30, "high", scheduled_time="08:00", pet_name="Rex", recurrence="daily")
    feed_task = Task("Feed breakfast", 10, "high", scheduled_time="07:00", pet_name="Rex")
    grooming_task = Task("Brush fur", 15, "medium", scheduled_time="09:00", pet_name="Whiskers", recurrence="weekly")
    playtime_task = Task("Play with laser pointer", 20, "low", scheduled_time="09:00", pet_name="Whiskers")

    # Let's mark one task complete already, so filter_by_status() has something to split on
    feed_task.mark_complete()

    # Now we would assign tasks to pets
    dog.add_task(walk_task)
    dog.add_task(feed_task)
    cat.add_task(grooming_task)
    cat.add_task(playtime_task)

    # With that done, let's gather all the tasks and run them through the Scheduler
    all_tasks = dog.get_tasks() + cat.get_tasks()
    scheduler = Scheduler(tasks=all_tasks, available_time=60)

    # Show the original task list before we sort or filter anything
    print("Original task list:")
    for task in scheduler.tasks:
        print(f"- {task.scheduled_time}: {task.describe_task()}")

    schedule = scheduler.generate_schedule()

    # Then we print a clean, readable summary
    print("=" * 40)
    print("Today's Schedule")
    print("=" * 40)
    print(f"Owner: {owner.name}")
    print(f"Pets: {', '.join(pet.name for pet in owner.pets)}")
    print(f"Available time: {scheduler.available_time} minutes")
    print("-" * 40)

    if schedule:
        for i, task in enumerate(schedule, start=1):
            print(f"{i}. {task.describe_task()}")
    else:
        print("No tasks fit in the available time.")

    print("-" * 40)
    total_time = sum(task.duration_minutes for task in schedule)
    print(f"Total scheduled time: {total_time} minutes")
    print("=" * 40)

    # Now let's see the tasks sorted by scheduled time
    print("\nTasks sorted by time:")
    for task in scheduler.sort_by_time():
        print(f"- {task.scheduled_time}: {task.describe_task()}")

    # Next, let's filter down to just Rex's tasks
    print("\nTasks for Rex:")
    for task in scheduler.filter_by_pet("Rex"):
        print(f"- {task.describe_task()}")

    # And now let's split tasks up by whether they're done or not
    print("\nCompleted tasks:")
    for task in scheduler.filter_by_status(True):
        print(f"- {task.describe_task()}")

    print("\nPending tasks:")
    for task in scheduler.filter_by_status(False):
        print(f"- {task.describe_task()}")

    # Here we expand out the recurring tasks to see what's coming up
    print("\nUpcoming recurring task copies:")
    for task in scheduler.expand_recurring_tasks(days=3):
        print(f"- {task.describe_task()}")

    # Finally, let's check for conflicts (grooming and playtime are both at 09:00)
    print("\nScheduling conflicts:")
    conflicts = scheduler.find_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"- {warning}")
    else:
        print("No conflicts found.")

    # Now let's demo automated recurrence: complete a daily task and roll it forward
    print("\nRecurring task demo:")
    daily_task = Task(
        "Give medication",
        5,
        "high",
        scheduled_time="08:30",
        pet_name="Rex",
        recurrence="daily",
        due_date=date(2026, 7, 5),
    )
    print(f"- Created: {daily_task.describe_task()} (due {daily_task.due_date})")

    daily_task.mark_complete()
    print(f"- Completed: {daily_task.describe_task()} (due {daily_task.due_date})")

    next_task = daily_task.create_next_occurrence()
    if next_task:
        print(f"- Next occurrence: {next_task.describe_task()} (due {next_task.due_date})")
    else:
        print("- No next occurrence generated.")


if __name__ == "__main__":
    main()
