import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
#pip install SQLAlchemy
db_path='pets_db.db'
st.set_page_config(
    page_title="CRUD",
    page_icon="🧊",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    },layout="wide"
)
#clead cach so that no need to refresh table when data modidied.
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
#st.cache_data.clear()
#st.cache_resource.clear()
#menu for CRUD
selected = option_menu(None, ["Add New", "View", "	Update", 'Delete'],
                        icons=['cloud-plus', 'list-task', "pencil-square", 'x-circle'],
                        key='menu_1', orientation="horizontal")
# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('pets_db', type='sql')

# CRUD functions
# add new
def add_new_record(owner,pet):
    
    message=True
    #st.write(owner,pet)
    try:
        with conn.session as s:
            s.execute(text(
                    'INSERT INTO pet_owners (person, pet) VALUES (:person,:pet);'),
                    params={"person":owner,"pet":pet},
                )
            s.commit()
        return message
    except Exception as e:
        #st.error(e)
        return e
    finally:
          s.close()

def add_new():
    placeholder = st.empty()
     
    with placeholder.container():
        with st.form(key="form1",clear_on_submit=True):
            owner=st.text_input("Owner Name",key="ownernme")
            pet=st.text_input("Pet Name",key="petrnme",)
            #stbutton=st.form_submit_button("Submit",on_click=add_new_record,kwargs={"owner":owner,"pet":pet})
            stbutton=st.form_submit_button("Submit")
            if stbutton:
                addrecord= add_new_record(owner,pet)
                #placeholder.empty()
                
                if addrecord==True:
                                st.toast("Record Added Successfully...Continue to Add more", icon="👍")
                                
                else:
                                
                                st.toast(f"Error:-{addrecord}", icon="👎")
                                st.toast("Try Again")
                    
         
# Vew data
def view_data():
    #st.cache_data.clear() required
    with conn.session as s:
            
            df=conn.query("select * from pet_owners")
            st.dataframe(df,hide_index=True,use_container_width=True)
    # with second option- No need to clear catch
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query="SELECT * from pet_owners"
        sql_query=pd.read_sql_query(query,sqliteConnection)
        userrights = pd.DataFrame(sql_query)
        cursor.close()
    except sqlite3.Error as error:
        userrights=error
        st.write(userrights)
    except :
        userrights="Run time Error...Invalid Input or Data type Mismatch" 
        st.error(userrights)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
            #message=("The SQLite connection is closed")
        st.dataframe(userrights,hide_index=True,use_container_width=True)

    # show selected Data 
    def dataframe_with_selections(df):
        df_with_selections = df.copy()
        df_with_selections.insert(0, "Select", False)

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )

        # Filter the dataframe using the temporary column, then drop the column
        selected_rows = edited_df[edited_df.Select]
        return selected_rows.drop('Select', axis=1)


    selection = dataframe_with_selections(df)
    st.write("Your selection:")
    st.write(selection)
    
# Modify data
def update_data():
    df=conn.query("select * from pet_owners")
    st.data_editor(df,hide_index=True,use_container_width=True,key="edit_data")
# Delet data
# get Selected dataframe

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        height=300
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def delete_data():
     message=""
     df=conn.query("select * from pet_owners")
     selection = dataframe_with_selections(df)
     delsection=st.empty()
     with delsection.container():
        if len(selection)>0:
            col1, col2= st.columns([3,1])
            with col1: 
                st.info("Are you Sure you want to Delete following rows:")
                st.dataframe(selection,hide_index=True)
            with col2:
                yesbutton=st.button("Yes",key="yes")
                mylist=selection["id"].tolist()
                tnewlist=tuple(mylist)
                #st.write(mylist)
                #st.write(tnewlist)
            if yesbutton:
                                try:
                                    with conn.session as s:
                                        #tuple with 1 vlue gives error eg(8,)
                                        if len(mylist)>1:
                                            s.execute(text(f'DELETE from pet_owners WHERE id In {tnewlist}')) 
                                        else:
                                            s.execute(text(f'DELETE from pet_owners WHERE id = {tnewlist[0]}'))        
                                        s.commit()
                                    message=True
                                except Exception as e:
                                    #st.error(e)
                                    message= e
                                finally:
                                    s.close()
                                delsection.empty()
        if message==True:
                                st.success("Records Deleted Successfully...")                  
        elif message=="" :
                                st.write("")
        else:
                                    st.error(message) 
                                    st.error("Try Again") 
                




if selected=="Add New":
    add_new()
elif selected=="View":
    #st.cache_resource.clear()
    view_data()
elif selected=="Update":
    st.cache_resource.clear()
    update_data()
else:
    st.cache_resource.clear()
    delete_data()
    