# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design for PawPal+ includes four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

The `Owner` class represents the person using the app. It stores basic information such as the owner’s name and preferences. The owner can have one or more pets.

The `Pet` class represents each pet that needs care. It stores information such as the pet’s name, species, and any care preferences or needs. Each pet can have multiple care tasks connected to it.

The `Task` class represents a pet care activity that needs to be completed. Each task has a title, duration in minutes, priority level, and possibly a preferred time. Examples of tasks include walking the dog, feeding the pet, grooming, or giving medication.

The `Scheduler` class is responsible for taking the list of tasks and creating a daily care plan. It will choose and order tasks based on constraints such as task duration, priority, and available time. It should also explain why each task was included in the schedule.

The main relationship in my design is that an `Owner` has one or more `Pet` objects, and each `Pet` can have many `Task` objects. The `Scheduler` uses the tasks from the pet and builds a final ordered schedule for the day.

Three core actions the user should be able to perform are:
1. Add a pet with basic information.
2. Add care tasks for the pet, including duration and priority.
3. Generate a daily schedule that organizes the tasks and explains the plan.

This design separates the data classes from the scheduling logic, which should make the program easier to read and extend. `Owner`, `Pet`, and `Task` are just plain data holders — they know how to store their own information and do small things like `mark_complete()` or `add_task()`, but none of them know how to build a schedule, sort anything, or check for conflicts. I kept it that way on purpose: an `Owner` shouldn't need to know how sorting works, and a `Task` shouldn't need to know it's being compared against other tasks. That's a job for something that can see the whole list at once.

That's why `Scheduler` owns all of the sorting, filtering, and conflict detection logic. Those operations all need to look across multiple tasks at the same time — sorting by time only makes sense in the context of a full task list, and you can't detect a conflict by looking at a single task in isolation. Putting that logic in one place also made testing much easier. Instead of having to test scheduling behavior through `Owner` or `Pet`, I could build a `Scheduler` directly with a small list of test tasks and check its output.

**b. Design changes**

My initial UML design was close to what I ended up building, but a few things changed once I started implementing. The biggest change was splitting what I originally thought of as one "build the schedule" method into several smaller, focused methods: `sort_by_time()`, `filter_by_pet()`, `filter_by_status()`, and `find_conflicts()`. Early on I imagined the scheduler doing everything in one big function, but that got hard to test and hard to reason about. Breaking it into small methods that each do one thing made it much easier to write a test for each behavior on its own.

I also added `recurrence` and `due_date` to `Task` partway through, along with `create_next_occurrence()` on `Task` and `expand_recurring_tasks()` on `Scheduler`. That wasn't in my original design — it came out of thinking about what a "smarter" scheduler should actually do for chores like medication or grooming that repeat on a schedule instead of being one-off tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler mainly considers three things: how long a task takes (`duration_minutes`), how important it is (`priority`), and how much time the owner actually has available (`available_time`). `generate_schedule()` sorts tasks by priority first, then fills up the available time with as many high-priority tasks as will fit before moving on to lower-priority ones. I decided priority and time were the two constraints that mattered most because they map directly to the real problem: a busy pet owner has a limited amount of time and needs to know what matters most gets done first, not just whatever was added to the list first.

**b. Tradeoffs**

One clear tradeoff I made is in `find_conflicts()`. Right now it only flags two tasks as conflicting if they share the exact same `scheduled_time` string, like two tasks both set at `"09:00"`. It does not detect overlapping durations — for example, a 30-minute task starting at 08:00 and another task starting at 08:15 would not be flagged, even though they actually overlap.

I chose exact-time matching instead of full overlap detection because it's much easier to read, test, and explain. The logic is just a string comparison between two values, so anyone reading `find_conflicts()` can understand what it does in a few seconds, and the tests for it are just as simple — I can hand it two tasks with the same `scheduled_time` and know exactly what should happen. Real overlap detection would mean parsing `"HH:MM"` strings into actual times, calculating start/end windows using `duration_minutes`, and checking whether those windows intersect, which adds real complexity for a feature I wasn't confident I could get fully correct and well-tested in the time I had. For this project, I'd rather ship a smaller feature that works reliably and that I can clearly explain than a bigger one I'm not sure is correct.

---

## 3. AI Collaboration

**a. How you used AI**

The AI features I leaned on the most were inline code suggestions while writing the `Scheduler` methods, and being able to ask direct questions like "what's a simple way to sort a list of tasks by a time string" or "how do I test that two tasks conflict." Those small, specific questions worked much better for me than asking for something broad like "build me a scheduler," because I still had to understand and adjust everything that came back. Debugging help was also useful — when a test failed because I was comparing `None` scheduled times, having something to talk through the traceback with helped me find the fix faster than staring at it myself.

**b. Judgment and verification**

One suggestion I didn't take as-is was around how to represent task times. It would have been reasonable to use Python's `datetime.time` objects instead of plain `"HH:MM"` strings, which is what a more "correct" implementation might do. I kept the simple string version instead, because for this project — with a beginner-friendly scope and a focus on exact-time conflict checks rather than full overlap math — strings were easier for me to reason about, easier to print in `describe_task()`, and easier to write tests against without pulling in more `datetime` handling than I needed. If I ever build the overlap-detection version of conflict checking, that's probably when switching to real time objects would actually pay off.

To verify things generally, I didn't just trust that code "looked right." I ran `python main.py` after each change to see the actual printed output, and I wrote or extended a pytest test for each new behavior — sorting, filtering, recurrence, and conflicts — so I had something concrete telling me whether the logic worked, not just my own read of the code.

**c. Working across sessions**

Using separate chat sessions for different phases of the project helped me stay organized because each session stayed focused on one problem instead of turning into one long conversation covering the whole project. I used one phase for the initial UML/class design, another for implementing the `Scheduler` methods, and another for writing tests and polishing the README. Keeping them separate meant I wasn't scrolling back through unrelated design discussion while trying to debug a failing test, and it made it easier for me to review each phase's output on its own before moving to the next one.

**d. Being the lead architect**

The biggest thing I learned is that AI is much more useful when I already know what I want the system to look like before I start asking for help. When I came in with a clear class breakdown — `Owner`, `Pet`, `Task`, `Scheduler` — and specific questions about one method at a time, the suggestions I got back were easy to evaluate and fit cleanly into the design. When I tried asking for something more open-ended, I got answers that were harder to check and didn't always match how I'd already structured things. I ended up thinking of AI less like something that designs the system for me, and more like a fast, knowledgeable pair partner — I still had to be the one deciding what the classes were, what belonged in `Scheduler` versus `Task`, and which tradeoffs were acceptable for this project.

---

## 4. Testing and Verification

**a. What you tested**

I ended up with six tests in `tests/test_pawpal.py`, covering the behaviors I was least willing to get wrong:

- **Task completion** — a new `Task` starts with `completed` set to `False`, and calling `mark_complete()` flips it to `True`.
- **Task addition** — adding a `Task` to a `Pet` increases that pet's task count from 0 to 1.
- **Sorting correctness** — `Scheduler.sort_by_time()` returns tasks in the right order (07:00, 08:00, 09:00) even when they were added out of order.
- **Recurrence logic** — completing a daily task and calling `create_next_occurrence()` produces a new task due exactly one day later, with `completed` reset to `False`.
- **Conflict detection** — two tasks scheduled at the same exact time produce at least one conflict warning.
- **Empty scheduler edge case** — calling `sort_by_time()` and `find_conflicts()` on a `Scheduler` with no tasks returns empty lists instead of crashing.

These mattered to me because they're the behaviors the whole app depends on. If sorting or conflict detection were silently wrong, the schedule shown to the user would look fine but actually be misleading, and that's a much worse failure than a crash — a crash you notice immediately, a silently wrong schedule you might not. The empty-list test mattered for a similar reason: a new user with no tasks yet is the very first thing someone sees when they open the app, so it needed to not blow up.

**b. Confidence**

I'm fairly confident — around 4 out of 5 — that the scheduler works correctly for everything the tests actually cover. Sorting, filtering, recurrence, and the empty-scheduler case all pass consistently and I've also watched them behave correctly in the `main.py` CLI output, not just in the tests. The point I'm holding back is conflict detection, since I know it only catches exact-time matches and not overlapping durations, so it's confident about a narrower guarantee than "no double-booking" — it's really "no two tasks at the identical timestamp."

If I had more time, the edge cases I'd test next are: two tasks with overlapping durations but different start times (the known gap), a task with no `scheduled_time` at all being sorted or checked for conflicts, and a weekly recurring task chained through multiple `create_next_occurrence()` calls to make sure the due dates keep advancing correctly instead of drifting.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how the `Scheduler` class turned out. Breaking it into small, single-purpose methods — `sort_by_time()`, `filter_by_pet()`, `filter_by_status()`, `find_conflicts()` — made the code easy to read and, just as importantly, easy to test. Each method does exactly one thing, so writing a test for it meant setting up a couple of tasks and checking one clear outcome, rather than untangling a big function that did everything at once.

**b. What you would improve**

If I had another iteration, I'd tackle the overlapping-duration conflict detection I mentioned in the tradeoffs section. I'd also want to validate `scheduled_time` input more (right now it's just a free-text `"HH:MM"` string with nothing stopping a typo like `"25:00"`), and add a way to persist tasks between runs of the Streamlit app instead of losing everything when the session ends.

**c. Key takeaway**

The biggest thing I learned is that good design decisions come from knowing what to leave out, not just what to add. Choosing simple `"HH:MM"` strings over `datetime.time` objects, and exact-time conflict checks over full overlap detection, weren't shortcuts I took because they were easier to code — they were deliberate choices to keep the system small enough that I could fully understand, test, and explain every part of it. That same idea carried over into working with AI: it was most helpful when I already knew the shape of what I wanted and used it to fill in one piece at a time, not when I asked it to design the whole thing for me.