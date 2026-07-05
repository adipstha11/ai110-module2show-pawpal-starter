"""Simple CLI demo for PawPal+.

Creates an owner with a couple of pets, gives them some tasks,
runs the Scheduler, and prints out a clean "Today's Schedule" view.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # 1. Create an owner
    owner = Owner("Alex", preferences="Prefers morning walks")

    # 2. Create two pets
    dog = Pet("Rex", "Dog")
    cat = Pet("Whiskers", "Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    # 3. Create at least three tasks with different titles, durations, and priorities
    walk_task = Task("Morning walk", 30, "high")
    feed_task = Task("Feed breakfast", 10, "high")
    grooming_task = Task("Brush fur", 15, "medium")
    playtime_task = Task("Play with laser pointer", 20, "low")

    # 4. Assign tasks to pets
    dog.add_task(walk_task)
    dog.add_task(feed_task)
    cat.add_task(grooming_task)
    cat.add_task(playtime_task)

    # 5. Gather all tasks and run them through the Scheduler
    all_tasks = dog.get_tasks() + cat.get_tasks()
    scheduler = Scheduler(tasks=all_tasks, available_time=60)
    schedule = scheduler.generate_schedule()

    # 6. Print a clean, readable summary
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


if __name__ == "__main__":
    main()
