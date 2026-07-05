import streamlit as st

from pawpal_system import Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

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
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a schedule from your saved tasks using the Scheduler backend.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above.")
    else:
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

        scheduler = Scheduler(tasks=tasks)

        st.markdown("#### Schedule (sorted by time)")
        for task in scheduler.sort_by_time():
            st.write(f"- {task.scheduled_time}: {task.describe_task()}")

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
            st.write("No conflicts found.")
