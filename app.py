import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. Enter your pet's info, add some
care tasks, then generate a smart schedule.
"""
)

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add care tasks for your pet. They'll feed into the scheduler below.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

scheduled_time = st.text_input("Time (HH:MM)", value="08:00")
recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])
completed = st.checkbox("Completed", value=False)

if st.button("Add task"):
    st.session_state.tasks.append(
        {
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": priority,
            "scheduled_time": scheduled_time,
            "pet_name": pet_name,
            "completed": completed,
            "recurrence": recurrence,
        }
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.dataframe(st.session_state.tasks, use_container_width=True)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a schedule from your saved tasks using the Scheduler backend.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above.")
    else:
        owner = Owner(owner_name)
        pet = Pet(pet_name, species)
        owner.add_pet(pet)

        tasks = [
            Task(
                title=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=t["priority"],
                scheduled_time=t["scheduled_time"],
                pet_name=t["pet_name"],
                recurrence=t["recurrence"],
            )
            for t in st.session_state.tasks
        ]
        for task, saved in zip(tasks, st.session_state.tasks):
            if saved["completed"]:
                task.mark_complete()
            pet.add_task(task)

        scheduler = Scheduler(tasks=tasks)

        st.success("Schedule generated!")

        st.markdown("#### Schedule (sorted by time)")
        sorted_tasks = scheduler.sort_by_time()
        st.table(
            [
                {
                    "Time": task.scheduled_time,
                    "Task": task.title,
                    "Pet": task.pet_name,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority,
                    "Status": "done" if task.completed else "pending",
                }
                for task in sorted_tasks
            ]
        )

        st.markdown("#### Pending tasks")
        pending = scheduler.filter_by_status(False)
        if pending:
            for task in pending:
                st.write(f"- {task.describe_task()}")
        else:
            st.write("None")

        st.markdown("#### Completed tasks")
        done = scheduler.filter_by_status(True)
        if done:
            for task in done:
                st.write(f"- {task.describe_task()}")
        else:
            st.write("None")

        st.markdown("#### Scheduling conflicts")
        conflicts = scheduler.find_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.info("No conflicts found.")
