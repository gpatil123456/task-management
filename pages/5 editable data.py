import streamlit as st
import sqlite3
import pandas as pd

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

edited_df = st.data_editor(df) # 👈 An editable dataframe

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
st.write("try copy past data to add new rows")
edited_df = st.data_editor(df,num_rows="dynamic") # 👈 An editable dataframe

df1=pd.DataFrame(
    columns=['Account','DR/CR','Amount','Date']
)
def checkcolums():
    st.write("change")

newdf=st.data_editor(df1,hide_index=True,num_rows="dynamic",
                     column_config={"DR/CR": st.column_config.SelectboxColumn(
                        "DR/CR",
                        help="The category of the app",
                        width="medium",
                        options=[
                            "📊 Data Exploration",
                            "📈 Data Visualization",
                            "🤖 LLM" ]
                            )},on_change=checkcolums
                    )