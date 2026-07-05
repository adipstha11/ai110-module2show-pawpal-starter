from datetime import timedelta


class Task:
    def __init__(
        self,
        title,
        duration_minutes,
        priority,
        scheduled_time=None,
        pet_name=None,
        recurrence="none",
        due_date=None,
    ):
        """Just setting up a new task here, starts off as not completed."""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.scheduled_time = scheduled_time
        self.pet_name = pet_name
        self.recurrence = recurrence
        self.due_date = due_date
        self.completed = False

    def mark_complete(self):
        """Flip this task over to completed."""
        self.completed = True

    def create_next_occurrence(self):
        """Return a new Task for the next occurrence (daily +1 day, weekly +7 days), or None if it doesn't recur."""
        if self.recurrence == "none" or self.due_date is None:
            return None

        if self.recurrence == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            next_due_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            scheduled_time=self.scheduled_time,
            pet_name=self.pet_name,
            recurrence=self.recurrence,
            due_date=next_due_date,
        )

    def get_priority(self):
        """Send back whatever priority we set for this task."""
        return self.priority

    def describe_task(self):
        """Put together a quick readable line about this task and return it."""
        status = "done" if self.completed else "pending"
        return f"{self.title} ({self.duration_minutes} min, priority: {self.priority}, {status})"


class Pet:
    def __init__(self, name, species):
        """Making a new pet, no tasks assigned yet so we start with an empty list."""
        self.name = name
        self.species = species
        self.tasks = []

    def add_task(self, task):
        """Toss a new task onto this pet's list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Just hand back this pet's list of tasks."""
        return self.tasks


class Owner:
    def __init__(self, name, preferences=""):
        """Setting up a new owner, no pets attached yet."""
        self.name = name
        self.preferences = preferences
        self.pets = []

    def add_pet(self, pet):
        """Add this pet to the owner's list of pets."""
        self.pets.append(pet)

    def view_schedule(self):
        """Go through every pet and print out all of their tasks."""
        for pet in self.pets:
            for task in pet.get_tasks():
                print(task.describe_task())


class Scheduler:
    def __init__(self, tasks=None, available_time=0):
        """Setting up the scheduler with the tasks we have and how much time we've got."""
        self.tasks = tasks if tasks is not None else []
        self.available_time = available_time

    def generate_schedule(self):
        """Sort tasks by priority and pack in as many as fit in the available time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 3))

        schedule = []
        remaining_time = self.available_time
        for task in sorted_tasks:
            if task.duration_minutes <= remaining_time:
                schedule.append(task)
                remaining_time -= task.duration_minutes
        return schedule

    def explain_plan(self):
        """Build the schedule and print out each task that made the cut."""
        schedule = self.generate_schedule()
        for task in schedule:
            print(f"Scheduled: {task.describe_task()}")

    def sort_by_time(self):
        """Return all tasks sorted by scheduled_time, earliest first."""
        return sorted(self.tasks, key=lambda t: t.scheduled_time)

    def filter_by_pet(self, pet_name):
        """Return only the tasks belonging to the given pet."""
        return [task for task in self.tasks if task.pet_name == pet_name]

    def filter_by_status(self, completed):
        """Return only the tasks matching the given completion status (True/False)."""
        return [task for task in self.tasks if task.completed == completed]

    def find_conflicts(self):
        """Return warnings for any tasks that share the exact same scheduled_time."""
        warnings = []
        for i in range(len(self.tasks)):
            for j in range(i + 1, len(self.tasks)):
                task_a = self.tasks[i]
                task_b = self.tasks[j]
                if task_a.scheduled_time == task_b.scheduled_time:
                    warnings.append(
                        f"Conflict: '{task_a.title}' and '{task_b.title}' "
                        f"are both scheduled at {task_a.scheduled_time}."
                    )
        return warnings

    def expand_recurring_tasks(self, days=7):
        """Generate future copies of recurring tasks.

        Daily tasks get one copy per day for the given number of days.
        Weekly tasks get a single copy 7 days later.
        """
        new_tasks = []
        for task in self.tasks:
            if task.recurrence == "daily":
                for day in range(1, days + 1):
                    new_tasks.append(self._copy_task(task, day))
            elif task.recurrence == "weekly":
                new_tasks.append(self._copy_task(task, 7))
        return new_tasks

    def _copy_task(self, task, days_ahead):
        """Make a copy of a task labeled with how many days ahead it occurs."""
        copy = Task(
            title=f"{task.title} (+{days_ahead}d)",
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            scheduled_time=task.scheduled_time,
            pet_name=task.pet_name,
            recurrence=task.recurrence,
        )
        return copy
