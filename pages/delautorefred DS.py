import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
#pip install SQLAlchemy

st.set_page_config(
    page_title="CRUD",
    page_icon="🧊",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.cache_data.clear()
#clead cach so that no need to refresh table when data modidied.
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('pets_db', type='sql')
if "df" not in st.session_state:
     st.session_state.df = pd.DataFrame()

def dataframe_with_selections():
    df_with_selections = st.session_state.df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=st.session_state.df.columns,key="seldf"
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def show_df():
     st.session_state.df=conn.query("select * from pet_owners")
     selection=dataframe_with_selections(st.session_state.df)
     return selection

def deldata(mylist,tnewlist):
    try:
                                    with conn.session as s:
                                        #tuple with 1 vlue gives error eg(8,)
                                        #st.write(mylist)
                                        if len(mylist)>1:
                                            s.execute(text(f'DELETE from pet_owners WHERE id In {tnewlist}')) 
                                        else:
                                            s.execute(text(f'DELETE from pet_owners WHERE id = {tnewlist[0]}'))        
                                        s.commit()
                                    message="Records Deleted Successfully..."
                                    #st.session_state.df=conn.query("select * from pet_owners")
    except Exception as e:
                                    #st.error(e)
                                    message= e
    finally:
                                    s.close()
                                    st.toast(f'{message}')
                                    st.session_state.df=conn.query("select * from pet_owners")
                                    #st.dataframe(st.session_state.df)
                                    #show_df()


def delete_data():
     selection=show_df()
     #selection = dataframe_with_selections(st.session_state.df)
     delsection=st.empty()
     with delsection.container():
        if len(selection)>0:
            col1, col2= st.columns([3,1])
            with col1: 
                st.info("Are you Sure you want to Delete following rows:")
                st.dataframe(selection,hide_index=True)
            with col2:
                
                mylist=selection["id"].tolist()
                tnewlist=tuple(mylist)
                #st.write(mylist)
                #st.write(tnewlist)
                yesbutton=st.button("Yes",key="yes",on_click=deldata,args=(mylist,tnewlist))
            
                 
                                

                
delete_data()
