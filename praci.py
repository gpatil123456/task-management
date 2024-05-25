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
                                'Id':'id',
                                'Start Date':'start',
                                'Due Date':'end',
                                'Owner':'resourcesid'
                                })

# Format 'start' and 'end' columns
dftask['start'] = dftask['start'].str.replace('_', 'T')
dftask['end'] = dftask['end'].str.replace('_', 'T')

# Extract resources
owner_lists = []
for owner_string in dftask['resourcesid']:
    owner_string = owner_string.strip("[]")
    emails = [email.strip().strip('"') for email in owner_string.split(",")]
    owner_lists.extend(emails)

# Create events from task data

# Set up calendar resources
# # Set up calendar resources
# calendar_resources = [{"id": resource, "title": title} for resource, title in zip(owner_lists, dftask['title'])]
# calendar_resources = [{"id": resource, "title": resource} for resource in owner_lists]
calendar_resources=dftask.resourcesid.unique()

# id = pd.DataFrame(calendar_resources, columns=['id'])
# id['title'] = id['id']
# id = id.reset_index(drop=True)
# my_records = id.to_dict(orient='records')

# calendar_events = []
# for index row in id.iterrows():
#     calendar_event = {
#         "id": row['id'],
#         "title": row['title']
#     }
  
#     calendar_events.append(calendar_event)
# st.write(calendar_events)
# print(calendar_events)
id = pd.DataFrame(calendar_resources, columns =['id'])
id['title'] = id['id']
id['Owner']=id['id']
id = id.reset_index(drop=True)
my_records =  id.to_dict(orient='records')

# my_records=id.T.to_dict('records')
calendar_events=[]
for index, row in id.iterrows():
    calendar_event = {
        "id": row['id'],
        "Owner":row['Owner'],
        "title":row['title'],      
    }
    calendar_events.append(calendar_event)
st.write(calendar_events)

calendar_options = {
    "editable": "true",
    "navLinks": "true",
    "resources": calendar_events,
    "selectable": "true",
    "initialDate": "2023-07-01",
    "initialView": "dayGridMonth",
}

# Set up calendar mode
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
events = []
for index, row in dftask.iterrows():
    event = {
        "title": row['title'],
        "start": row['start'],
        "end": row['end'],
        "groupId": row['groupId'],  
        "resourcesid": row['resourcesid'] 
    }
    events.append(event)
st.write(events)
if "resource" in mode:
    calendar_options["resourceGroupField"] = "title"

if mode == "daygrid":
    calendar_options["headerToolbar"] = {
        "left": "today prev,next",
        "center": "title",
        "right": "dayGridDay,dayGridWeek,dayGridMonth",
    }
elif mode == "timegrid":
    calendar_options["initialView"] = "timeGridWeek"
elif mode == "timeline":
    calendar_options["headerToolbar"] = {
        "left": "today prev,next",
        "center": "title",
        "right": "timelineDay,timelineWeek,timelineMonth",
    }
    calendar_options["initialView"] = "timelineMonth"
elif mode == "list":
    calendar_options["initialView"] = "listMonth"
elif mode == "multimonth":
    calendar_options["initialView"] = "multiMonthYear"

# Set up Streamlit columns
col1, col2 = st.columns([8, 2])

with col1:
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

    if state.get("eventsSet") is not None:
        st.session_state["events"] = state["eventsSet"]

with col2:
    if state.get("eventClick") is not None:
        event_info = state["eventClick"].get("event")
        if event_info:
            st.write("Clicked Event:", event_info)
            st.write("Event Resources:", event_info.get("resources"))
