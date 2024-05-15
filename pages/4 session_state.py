import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Sessions",
    page_icon="🧊",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    },layout="wide"
)

with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
if "attendance" not in st.session_state:
        st.session_state.attendance = set()
if "formerror" not in st.session_state:
     st.session_state.formerror=""

def take_attendance():
        if st.session_state.name in st.session_state.attendance:
            st.info(f"{st.session_state.name} has already been counted.")
            st.session_state.formerror=f"{st.session_state.name} has already been counted."
        else:
            st.session_state.attendance.add(st.session_state.name)
            st.success(f"{st.session_state.name} Present")
            st.session_state.formerror=""

tab1,tab2,tab3,tab4,tab5=st.tabs(["form attendence","cahnge values","Buttons to add other widgets","form submit","Dynamic widgets"])
with tab1:
    
    with st.form(key="my_form"):
        st.text_input("Name", key="name")
        st.form_submit_button("I'm here!", on_click=take_attendance)
    if st.session_state.formerror: st.error(st.session_state.formerror)
    st.info(st.session_state.name)
    st.success(st.session_state.attendance)
with tab2:
    st.subheader("tab2")
    
    begin = st.container()

    if st.button('Clear name',key="b1"):
        st.session_state.tname = ''
    if st.button('Streamlit!',key="b2"):
        st.session_state.tname = ('Streamlit')

    # The widget is second in logic, but first in display
    begin.text_input('Name', key='tname')

with tab3:
#Buttons to add other widgets dynamically
    cont = st.empty()
    
    #for enabling  button default true
    if 'b1_enable' not in st.session_state:
            st.session_state.b1_enable=True
            #st.write(st.session_state[f'delet_b{k}'])
     #for total check
    if "b1_total" not in st.session_state:
            st.session_state.b1_total=0
  
    with cont.container(border=True):
        
        def decrease_rows(k):
            #st.session_state['rows'] -= 1
            del st.session_state[f'first_{k}']
            del st.session_state[f'middle_{k}']
            del st.session_state[f'last_{k}']
            del st.session_state[f'delet_b{k}']
            st.session_state['rows'].remove(k)
            #st.success(st.session_state['rows'])
            #if no rows set total to 0
            if len(st.session_state['rows'])==0:
                 st.session_state.b1_total=0
            

        left, middle, right ,delet_b= st.columns(4)
        left.success(":green[**Account**]")
        middle.success(":green[**Amount**]")
        right.success(":green[**Dr/CR**]")
        delet_b.error("Remove")

        if 'rows' not in st.session_state:
            st.session_state['rows'] = [0]
        
        def display_input_row(index):
                left, middle, right ,delet_b= st.columns(4)
                
                left.selectbox('',("A","B","C"), key=f'first_{index}',label_visibility="collapsed",)
                middle.number_input('',step=1.00, key=f'middle_{index}',label_visibility="collapsed")
                right.selectbox('',options=["Dr","Cr"], key=f'last_{index}',label_visibility="collapsed")
                delet_b.button(":red[**X**]",key=f'delet_b{index}',on_click=decrease_rows,args=(index,))
                
        def increase_rows():
            if len(st.session_state['rows'])>0:
                nrow=1+max(st.session_state['rows'])
            else:
                 nrow=0
                 
            st.session_state['rows'].append(nrow)
            #checktotal()
            
        #list all row
        for i in st.session_state['rows']:
            display_input_row(i)
        #check if all form is proper then only Enable button by changing session state
        total=0
        for i in st.session_state['rows']:
            total=total+st.session_state[f'middle_{i}']
            #st.write(st.session_state[f'middle_{i}'])
            #st.write(total)
        st.session_state.b1_total=total
                    
        #enable Button 
        if st.session_state.b1_total==0:

            st.session_state.b1_enable=False
            st.write(f':blue[Total: {st.session_state.b1_total}]')
        else:
            st.session_state.b1_enable=True
            st.write(f':red[Total must be 0. Current Total is: {st.session_state.b1_total}]')
                
        
        st.button('Add person', on_click=increase_rows,key='bincre',disabled=st.session_state.b1_enable)
        
            
    # Show the results
    st.subheader('Data')
    for i in st.session_state['rows']:
        st.write(
            f'Record {i+1}:',
            st.session_state[f'first_{i}'],
            st.session_state[f'middle_{i}'],
            st.session_state[f'last_{i}'],
            st.session_state.b1_total,
            st.session_state.b1_enable
        )
with tab4:
    # Initialize disabled for form_submit_button to False
    #if "disabled" not in st.session_state:
        #st.session_state.disabled = True
    #def showform():
        def clear_fields():
             clearfields=["namest","namest1","namest2"]
             allfields= False
             for i in clearfields:
                  if len(st.session_state[f'{i}'])<1:
                       allfields=True
             #if (len(names)<1 or len(names1)<1 or len(names2)<1):
             if allfields:
                st.toast("Enter All Manadtory Fields *")
             else:
                st.toast("Record Added Successfully...")
                for i in clearfields:
                        #st.write(st.session_state[f'{i}'])
                        st.session_state[f'{i}']=""
                        #st.write("after")
                        #st.write(st.session_state[f'{i}'])

        with st.form("myform",clear_on_submit=False):
            # Assign a key to the widget so it's automatically in session state
            names = st.text_input(f"Enter your name below: :red[*]", key="namest",)
            names1 = st.text_input("Enter your name below:", key="namest1")
            names2 = st.text_input("Enter your name below:", key="namest2")
            slider=st.slider("enetr",key="slider")
                           
            submit_button = st.form_submit_button("Submit",on_click=clear_fields)
        
with tab5:
    cc_cont=st.empty()
    
    with cc_cont.container(border=True):
        st.subheader("Cost Center Details...")
        #get Cost centers & categories list
        ccat=["AAA","BBB","CCC"]
        ccA=["aaAAA","aaBBB","aaCCC"]
        ccB=["bbAAA","bbBBB","ccCCC"]
        ccC=["ccAAA","ccBBB","ccCCC"]
        
        #for each Ledger- Add Cost Center & Cost Category
        for i in st.session_state['rows']:
            #st.session_state[f'first_{i}']
            #add expander with Ledgername
            exp_name=f'{i}_{st.session_state[f"first_{i}"]}'
            #st.write(exp_name)
            exp_name=st.expander(f":blue[**Allocation for:-{st.session_state[f'first_{i}']}**] :- :green[**{st.session_state[f'middle_{i}']}**]",expanded=False)
            #for each Ledget in expander add CC details
            
            with exp_name:
                 #exp_name. write(f"Cost Category -{st.session_state[f'first_{i}']}")
                 #for each cost category
                 for cc in ccat:
                    if cc=="AAA":
                        Costcenter=ccA
                    elif cc=="BBB":
                        Costcenter=ccB
                    else:
                        Costcenter=ccC

                    st.write(f"Cost Category- {cc}")
                    df1=pd.DataFrame(
                            columns=['Cost Center','Amount']
                        )
                    
                    newdf=st.data_editor(df1,hide_index=True,num_rows="dynamic",key=f"{cc}{i}_{st.session_state[f'first_{i}']}",
                                            column_config={"Cost Center": st.column_config.SelectboxColumn(
                                                "Cost Center",default=None,
                                                help="The category of the app",
                                                width="medium",required=True,
                                                options=Costcenter),
                                                "Amount" : st.column_config.NumberColumn(
                                                "Amount",default=0.00,required=True,format="%.2f",
                                                width="medium")
                                                
                                                    }
                                                    )
                    Total_amt = newdf['Amount'].sum()
                    if Total_amt> st.session_state[f'middle_{i}']:
                        st.write(f':red[Total Cost Center Amount must be Less Than or Equal to Ledget Amount]')
                    if (newdf['Cost Center']==None).values.any():
                         st.write(f':red[Cost Center can not Be Null...Please fill up all Cos Centers]')
                    ch=sum(pd.isnull(newdf['Cost Center']))
                    if ch:
                         st.write(ch)
                    
