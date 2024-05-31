import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from taskfunction import get_task_list

st.set_page_config(page_title="Demo for streamlit-calendar", page_icon="📆", layout="wide")

# Fetch task list
dftask = get_task_list()

# Rename column names
dftask = dftask.rename(columns={'Task': 'groupId', 
                                'Task_Details': 'title',
                                'Id': 'id',
                                'Start Date': 'start',
                                'Due Date': 'end',
                                'Owner': 'resourceId'
                                })

# Format 'start' and 'end' columns
dftask['start'] = dftask['start'].str.replace('_', 'T')
dftask['end'] = dftask['end'].str.replace('_', 'T')

# Set up calendar resources
calendar_resources = dftask[['groupId', 'resourceId']].drop_duplicates()

# Create events from task data
events = []
for index, row in dftask.iterrows():
    event = {
        "title": row['title'],
        "start": row['start'],
        "end": row['end'],
        "id": row['id'],
        "resourceId": row['resourceId']
    }
    events.append(event)

# Create calendar resources from task data
calendar_resources_list = []
for _, resource in calendar_resources.iterrows():
    calendar_resource = {
        "id": resource['resourceId'],       # Resource ID
        "title": resource['resourceId'],    # Resource title
    }
    calendar_resources_list.append(calendar_resource)

# Set up calendar options
calendar_options = {
    "editable": True,
    "navLinks": True,
    "resources": calendar_resources_list,
    "selectable": True,
    "initialDate": "2023-07-01",
    "initialView": "dayGridMonth",
    "resourceAreaHeaderContent": "Resource"
}

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "resource-daygrid",
        "resource-timegrid",
        "resource-timeline",
        "list",
        "multimonth",
    ),
)

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options.update({
            "initialDate": "2023-07-01",
            "initialView": "resourceDayGridDay",
        })
    elif mode == "resource-timeline":
        calendar_options.update({
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": "2023-07-01",
            "initialView": "resourceTimelineDay",
        })
    elif mode == "resource-timegrid":
        calendar_options.update({
            "initialDate": "2023-07-01",
            "initialView": "resourceTimeGridDay",
        })
else:
    if mode == "daygrid":
        calendar_options.update({
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": "2023-07-01",
            "initialView": "dayGridMonth",
        })
    elif mode == "timegrid":
        calendar_options.update({
            "initialView": "timeGridWeek",
        })
    elif mode == "timeline":
        calendar_options.update({
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timelineDay,timelineWeek,timelineMonth",
            },
            "initialDate": "2023-07-01",
            "initialView": "timelineMonth",
        })
    elif mode == "list":
        calendar_options.update({
            "initialDate": "2023-07-01",
            "initialView": "listMonth",
        })
    elif mode == "multimonth":
        calendar_options.update({
            "initialView": "multiMonthYear",
        })

# Render the calendar
state = calendar(
    events=st.session_state.get("events", events),
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)

# Update session state with new events if modified
if state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

# Display API reference
# st.markdown("## API reference")
# st.help(calendar)
