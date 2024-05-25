
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from taskfunction import get_task_list

def Gantt_Chart():
    placeholder = st.empty()
    with placeholder.container():
        st.subheader("Gantt chart")
        dftask=get_task_list()
        print(dftask)
        df = pd.DataFrame(dftask,columns=['Task', 'Task_Details','Start Date','Owner','Priority','Status', 'Due Date'])
        
# Convert Start and Finish columns to datetime
        df['Start Date'] = pd.to_datetime(df['Start Date'], format='%Y-%m-%d_%H:%M:%S')
        df['Due Date'] = pd.to_datetime(df['Due Date'], format='%Y-%m-%d_%H:%M:%S')
        option=st.selectbox("select option",options=['By Priority','By Owner','By Status'],key="option_menu")
        
# Plot Gantt chart
        
        if option=="By Priority":
           selected_color="Priority"
        elif option=="By Owner":
           selected_color="Owner"
        else: 
           selected_color="Status"   
        fig = px.timeline(df, x_start='Start Date', x_end='Due Date', y='Task',color=selected_color,opacity=0.5)
        fig.update_yaxes(categoryorder='total ascending')  # Order tasks by start time
        fig.update_layout(title='Gantt Chart')
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)

# Close connection to SQLite database

