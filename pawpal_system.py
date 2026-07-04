class Task:
    def __init__(self, title, duration_minutes, priority):
        """Just setting up a new task here, starts off as not completed."""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.completed = False

    def mark_complete(self):
        """Flip this task over to completed."""
        self.completed = True

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
