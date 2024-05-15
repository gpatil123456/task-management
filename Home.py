import streamlit as st
import re
import pandas as pd
import datetime
import secrets
import string
from datetime import date,timedelta
from streamlit_option_menu import option_menu
import random   
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
from functions import  update_password, del_lic,check_login,send_email_notification,update_users,add_new_license,generate_otp,get_licen,send_email_notification,send_email
def generate_password(len):  
    "This function accepts a parameter 'len' and returns a randomly generated password"  
  
    # defining the list of characters that will be used to generate the password  
    list_of_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"  
    selected_char = random.sample(list_of_chars, len)  
  
    # converting the list into the string  
    pass_str = "".join(selected_char)  
      
    # returning the generated password string  
    return pass_str   
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout='wide'
)
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
#st.markdown("""---""")
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
superadmin_con = st.container()
today=datetime.datetime.now()
def generate_random_password(length=10):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password
def show_login_page():
    with loginSection:
        tab1,tab2 =st.tabs(["Existing Users","Reset Password"])
        with tab1:
            # if 'loginerror' not in st.session_state:
            #     st.session_state['loginerror'] = ""
            if st.session_state['loggedIn'] == False:
                #it means no login then only go ahead
                st.title("Login") 
                userName = st.text_input (label="User ID", value="", placeholder="Enter your email",key="k1")
                     #get Companies for user
                password = st.text_input (label="Password", value="",placeholder="Enter password", type="password",key="k2")
                if userName=="superadmin":
                    if len(password)>0 and len(userName)>1:
                        st.button ("Login", key="supadminbutton",on_click=check_login, args= (userName, password,"AceProcure","superadmin"))
                else:
                    
                    if(re.fullmatch(regex, userName)):
                        # rights=get_user_rights()
                        #st.session_state['loginerror'] = ""
                        # mask = rights['username'] == userName
                        #st.write(mask)
                        # comp_name= rights[mask]
                        #comp_name=comp_name['company_name']
                        # compname=st.selectbox("Select Company",comp_name['company_name'])
                        # mask1=comp_name['company_name']==compname
                        # #st.write(mask1)
                        # roleds=comp_name[mask1]
                        # #st.write(roleds)
                        # if roleds.size !=0:
                        #     role=roleds['Role'].values[0]
                        # else:
                        #     role=""
                        # print(userName)
                        if len(password)>0 and len(userName)>1 :
                            st.button ("Login", on_click=check_login, args= (userName, password,))
                    else:
                        if len(userName)>1:
                            #st.session_state['loginerror'] = "Login Id must be an email"
                            st.toast("Invalid User Id... User Id must be in Email format.")
            #st.toast(f'Error:- {st.session_state['loginerror']}')
                #if userName=="admin" and password=="AcePro":
                #     st.button ("Login", on_click=check_login, args= (userName, password,compname,role))
                # else:
                #     st.button ("Login", on_click=check_login, args= (userName, password,compname,role))
        with tab2:
         
                
             if not st.session_state.get('show_otp', False) and not st.session_state.get('show_reset_password', False):
                email = st.text_input(label="Email", value="", placeholder="Enter your email")
                if st.button("Submit"):
                    if email: # Only proceed if email is not empty
                        # Logic for sending OTP
                        # Assuming you have a function to send OTP
                        otp = generate_otp()  # Generate OTP
                        send_email(sender_email="gauravpatil290198@gmail.com", receiver_email=email,subject="Reset Password OTP", body = f"""
    <html>
      <head></head>
      <body>
         <p>reset password- OTP is<span  style="color: blue;font-weight: bold;"> {otp},</span></p>
      </body>
    </html>
    """, password="kcxqtnnxxqgohuqq")

                        st.session_state['otp'] = otp
                        st.session_state['email'] = email
                        st.session_state['show_otp'] = True

            # Second condition: OTP text and button shown if email is correct.
             if st.session_state.get('show_otp', False):
                otp = st.text_input(label="OTP", value="", placeholder="Enter OTP")
                if st.button("Submit OTP"):
                    if otp == st.session_state['otp']:
                         st.session_state['show_otp'] = False
                         st.session_state['show_reset_password'] = True
                    else:
                         st.error("Wrong OTP. Please try again.")

            # Third condition: Show new password and re-enter password fields and a submit button if OTP is correct.
             if st.session_state.get('show_reset_password', False):
                new_password = st.text_input(label="New Password", value="", type="password")
                re_enter_password = st.text_input(label="Re-enter Password", value="", type="password")
                if st.button("Submit New Password"):
                    if new_password == re_enter_password:
                        # Logic to update password
                        update_password(new_password, st.session_state['email'])
                        st.success("Password updated successfully!")
                        st.session_state['show_reset_password'] = False
                    else:
                        st.error("Passwords do not match. Please try again.")


def show_view():
    st.success("show_view")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    #loginuser=""

def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.sidebar.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)

def show_admin():
    st.success("Admin")

def add_new_lic():
    placeholder = st.empty()
    def newlice(names,role,emails):
     
        #1st check email
        if(re.fullmatch(regex, emails)):
             clearfields=["tnamelic","licemail"]
             allfields= False
             for i in clearfields:
                  if len(st.session_state[f'{i}'])<1:
                       allfields=True
             #if (len(names)<1 or len(names1)<1 or len(names2)<1):
             if allfields:
                st.toast("Enter All Manadtory Fields *")
             else:
                lens = 8 
                pass_str = generate_password(lens) 
    # printing the generated password  
                print("A randomly generated Password is:", pass_str)

                #now add record
                addrecord= add_new_license(emails,pass_str,role,names)
                #placeholder.empty()
                print(addrecord)
                if addrecord==True:
                    send_email_notification(emails,names,pass_str)
                    st.toast("Record Added Successfully...Continue to Add more", icon="👍")
                                
                else:
                    st.toast(f"Error:-{addrecord}", icon="👎")
                    st.toast("Try Again")
                #clear text fields on form
                for i in clearfields:
                        #st.write(st.session_state[f'{i}'])
                        st.session_state[f'{i}']=""
        else:
            #st.toast(email)
            st.toast("email not in Proper format...")


    with placeholder.container(border=True):
        
        st.subheader("Add New License")
        
        names=st.text_input(f"Enter Name :red[*]",key="tnamelic")

        role = st.selectbox(
        "Enter The Role",
        ("Manager", "Executive"),
        index=0,  # Set the initial selection to "Manager"
        key="trole"
        )

# Now you can use the 'role' variable to access the selected value
        # st.write("Selected Role:", role)
       
  
    
         
        # passwords=st.number_input("Enter Time Difference",min_value=-720,max_value=840,value=0,key="ntime")
        emails=st.text_input(f"email :red[*]",key="licemail")
        # st.session_state.random_password = generate_random_password()   
        st.button("Submit",on_click=newlice,
                                args=[st.session_state.tnamelic,st.session_state.trole,st.session_state.licemail])
        
def view_data_lic():
    vew_lic_con  = st.empty()
    with vew_lic_con.container(border=True):
        st.subheader("List of License")
        df=get_licen()
        if isinstance(df, pd.DataFrame):
            st.dataframe(df,hide_index=True)
        else:
            st.toast(df)
            st.toast("error")
        
def update_data_lic():
    update_lic_con  = st.empty()
    
    def updatelic(emails,role,names):
        uplic= update_users(emails,role,names)
                #placeholder.empty()
                
        if uplic==True:
            st.toast("Record Updated Successfully...", icon="👍")
            st.session_state.selemail="------"
                        
        else:
            st.toast(f"Error:-{uplic}", icon="👎")
            st.toast("Try Again")
        
    with update_lic_con.container(border=True):
        st.subheader("Update License")
        df=get_licen()
        email_list = df["Username"].tolist()
        role_list=df["Role"].tolist()
        #add item                      at beginning of list 
        email_list.insert(0,"------")
        # st.session_state.mroles="------"

        email_sel=st.selectbox("Select email to Update Record",options=email_list,key="selemail",placeholder="Choose as Option")
        if email_sel !="------":
            #get data for selected email& show as default value of widgets
            name=df.query(f"Username=='{email_sel}'")["Name"].item()
            # Expiry_Date=df.query(f"Username=='{email_sel}'")["Expiry_Date"].item()
            # role=df.query(f"Username=='{email_sel}'")["Role"].item()
            #st.write(name,Expiry_Date,time_zone)
            mname=st.text_input(f"Update Name :red[*]",value=name,key="upname")
            # mrole=st.text_input(f"Update Role :red[*]",value=role,key="uprole")
            # mrole = st.selectbox(label="Update Role:" , index=0, key="uprole")
            mrole=st.selectbox("Select Role to Update Record",options=role_list,key="",placeholder="Choose as Option")

            # mrole=st.text_input(f"Update Role":red[*]",value=role,key="uprole")
            # mtime=st.number_input("Update Time Zoe",value=time_zone,min_value=-720,max_value=840,key="upntime")
            if len(mname)>1:
                # st.button("Update",key="upadtelic",on_click=updatelic,args=[mname,mExpiry_Date,mtime,email_sel])
                  st.button("Update",key="upadtelic",on_click=updatelic,args=[email_sel,mrole,mname])
def get_df():
    df=get_licen()
    if isinstance(df, pd.DataFrame):
        
        return df
    else:
        
        st.toast("error")
        return False
if "df" not in st.session_state:
     st.session_state.df = pd.DataFrame()

def delete_data_lic():
    del_lic_con  = st.empty()

    
# def updatelic(names,email):
    
    with del_lic_con.container(border=True):
        st.subheader("Delete License")
        st.info("Select Rows to Delete...")
        df=get_df()
        if df is False:
            st.toast(df)
        else:
            # Get dataframe row-selections from user with st.data_editor
            df.insert(0, "Select", False)
            edited_df = st.data_editor(
                df,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                disabled=st.session_state.df.columns,key="seldfdel"
            )
            # Filter the dataframe using the temporary column, then drop the column
            selected_rows = edited_df[edited_df.Select]
            selected_rows= selected_rows.drop('Select', axis=1)
            if len(selected_rows)>0:
                col1, col2= st.columns([3,1])
                with col1: 
                    st.error("Are you Sure you want to Delete following rows:")
                    st.dataframe(selected_rows,hide_index=True)
                with col2:
                    # mylist = selected_rows["Id"].tolist()
                    mylist = selected_rows["Id"].tolist()
                    myusername=selected_rows["Username"].tolist()
                    print(myusername)
                    print(mylist)
                    # tnewlist=tuple(mylist)
                    #st.write(mylist)
                    #st.write(tnewlist)
                    yesbutton=st.button("Yes",key="yes",on_click=del_lic,args=(mylist,myusername))
            

def show_superadmin():
    with superadmin_con:
        #st.success("Super Admin")
        with st.sidebar:
            sel=option_menu(menu_title="",options=["With Tabs"],
                            )
        # if sel=="Manage License":
           
        #     selected = option_menu(None, ["Add New", "View", "Update", 'Delete'],
        #                 icons=['cloud-plus', 'list-task', "pencil-square", 'x-circle'],
        #                 key='menu_1', orientation="horizontal")
            
        #     if selected=="Add New":
        #         add_new_lic()
        #     elif selected=="View":
        #         #st.cache_resource.clear()
        #         view_data_lic()
        #     elif selected=="Update":
                
        #         update_data_lic()
        #     else:
                
        #         delete_data_lic()
        st.success("Welcome" + st.session_state['Name'])
        st.success(st.session_state['Role'])
        st.success(st.session_state['Username'])
        
        if st.session_state['Role'] == "Manager":
            # If the user role is Manager, show tabs for managing licenses
            add_t, view_t, modify_t, del_t = st.tabs(["✔️**Add New**", "📋**View**", "✏️**Update**", "❌Delete"])
            with add_t:
                add_new_lic()
            with view_t:
                view_data_lic()
            with modify_t:
                update_data_lic()
            with del_t:
                delete_data_lic()
        if st.session_state['Role'] == "Executive":
            # add_t, view_t, modify_t, del_t = st.tabs(["✔️**Add New**", "📋**View**", "✏️**Update**", "❌Delete"])
            # with view_t:
                  st.write( st.session_state['Name'])  # Debug statement to confirm execution

              
            # If the user role is Executive, only show the superadmin view
                  view_data_lic()  # Or any other function to show the view

def show_main_page():
    st.success("show_main_page")

# def show_manager():
#     st.success("show_manager")

with headerSection:
    # for login checking
    if 'User' not in st.session_state:
        st.session_state['User'] = ""
    
    if 'Company' not in st.session_state:
        st.session_state['Company'] = ""
    
    if 'Role' not in st.session_state:
        st.session_state['Role'] = ""
    
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
                
    else:
        if st.session_state['loggedIn']:
            show_logout_page()   
            if st.session_state['Role'] == "View":
                show_view()
            elif st.session_state['Role'] == "Manager":
                show_superadmin()
            #    show_manager() 
            elif st.session_state['Role'] =="Executive":
                # show_admin()
                show_superadmin()
            elif st.session_state['Role'] =="superadmin":
                show_superadmin()
            else:
                show_main_page()   
        else:
            show_login_page()
# ?email- Welcome{name}, new user- default password-reset password- OTP is 1234