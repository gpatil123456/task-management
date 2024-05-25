import streamlit as st
import re
import pandas as pd
import datetime
from datetime import date, timedelta
from functions import get_licen
from taskfunction import addrecord_task
import json
from taskfunction import get_task_list, del_task, update_task

# Make a regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
today = datetime.datetime.now()

def delete_data_task_executive():
    st.error("you are not authorized deleted task")
def add_new_task():
    placeholder = st.empty()

    def add_task(task, task_Details, bucket, values_jsonowner, concatenated_starttime, concatenated_duetime, status, completion_stage, uploadedname, task_group, priority, plan_type, nature, timing, extent, actual_timing, actual_extent, created_by, concatenated_createdon):
        # Check email format
        if selected_emails and re.fullmatch(regex, selected_emails[0]):
            # Define the mandatory fields
            clearfields = [task]
            # Check if all mandatory fields are filled
            allfields = all(len(st.session_state[f'{i}']) > 0 for i in clearfields if f'{i}' in st.session_state)
            if not allfields:
                st.toast("Enter All Mandatory Fields (*)")
            elif start_date and start_time and due_date and due_time:
                if start_date == due_date and due_time <= start_time:
                    st.toast("Due date and time must be after start date and time.")
                else:
                    addrecord = addrecord_task(task, task_Details, bucket, values_jsonowner, concatenated_starttime, concatenated_duetime, status, completion_stage, uploadedname, task_group, priority, plan_type, nature, timing, extent, actual_timing, actual_extent, created_by, concatenated_createdon)
                    if addrecord:
                        st.toast("Record Added Successfully...Continue to Add more", icon="👍")
                        # Clear text fields on form
                        for i in clearfields:
                            st.session_state[f'{i}'] = ""
                    else:
                        st.toast(f"Error: {addrecord}")
                        st.toast("Try Again")
        else:
            st.toast("Email not in Proper format...")

    with placeholder.container():
        st.subheader("Add New License")

        ttaskdeatails=None
        task = st.text_input("Enter Task:red[*]")
        task_Details = st.text_input("Enter Task Details:red[*]", key="ttaskdeatails")
        bucket = st.text_input("Enter Bucket:red[*]", key="tbucket")
        df = get_licen()
        email_list = df["Username"].tolist() if not df.empty else []  # Ensure email_list is not empty
        email_list.insert(0, "------")

        usernameowner = st.multiselect("Select Owner", options=email_list, key="towner", placeholder="Choose as Option", default=[])
        values_jsonowner = json.dumps(usernameowner)
        selected_emails = json.loads(values_jsonowner)
        max_date = min(datetime.date(2034, 5, 16), today.date())

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=today.date())
            start_time = st.time_input("Start Time", key="tstart")
        with col2:
            due_date = st.date_input("Due Date", key="tdue")
            due_time = st.time_input("Due Time", key="tstart_due")
        concatenated_starttime = f"{start_date}_{start_time}"
        concatenated_duetime = f"{due_date}_{due_time}"

        status_options = ["Not Started", "In Progress", "Completed"]
        status = st.selectbox("Select Status:", options=status_options, index=0)
        completion_stage = st.number_input("Enter Completion Stage Percentage(%)", min_value=0, max_value=100, value=0, key="ime")

        uploaded_files = st.file_uploader("Choose a file", type=['docx', 'xlsx', 'pdf', 'jpeg', 'png', 'jpg'], accept_multiple_files=True)
        uploadedname = None

        for uploaded_file in uploaded_files:
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H-%M")
            name, extension = uploaded_file.name.rsplit('.', 1)
            file_with_timestamp = f"{name}_{formatted_datetime}.{extension}"
            uploadedname = file_with_timestamp

        task_group = st.text_input("Enter task group", key="taskgroup")
        priority_option = ["Medium", "Low", "Critical", "High"]
        priority = st.selectbox("Enter The Priority", options=priority_option, index=0)

        current_datetime = datetime.datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M")
        created_by = st.session_state.get('Name', 'Unknown')
        concatenated_createdon = f"{current_date}_{current_time}"

        plan_type = st.radio("Enter The Plan Type", ["Overall Audit Plan", "Audit Procedures"], index=0, horizontal=True, key="horizontal_rb")

        nature = timing = extent = actual_timing = actual_extent = None

        if plan_type == "Audit Procedures":
            nature = st.selectbox("Enter The Nature", ("Vouching", "Verification", "Confirmation", "Reconciliation", "Analysis", "Observation", "Enquiry"))
            timing = st.text_input("Enter Timing", key="timings")
            extent = st.text_input("Enter Extent", key="Extent")
            actual_timing = st.text_input("Enter Actual Timing", key="ATiming")
            actual_extent = st.text_input("Enter Actual Extent", key="AExtent")

        if st.button("Submit"):
            add_task(task, task_Details, bucket, values_jsonowner, concatenated_starttime, concatenated_duetime, status, completion_stage, uploadedname, task_group, priority, plan_type, nature, timing, extent, actual_timing, actual_extent, created_by, concatenated_createdon)


def view_data_task():
    vew_lic_con  = st.empty()
    with vew_lic_con.container(border=True):
        st.subheader("List of Task")
        df=get_task_list()
        if isinstance(df, pd.DataFrame):
            st.dataframe(df,hide_index=True)
        else:
            st.toast(df)
            st.toast("error")
def delete_data_task():
    del_lic_con  = st.empty()
    with del_lic_con.container(border=True):
        st.subheader("Delete License")
        st.info("Select Rows to Delete...")
        df=get_task_list()
        if df is False:
            st.toast(df)
        else:
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
                    tnewlist=tuple(mylist)
                    myusername=selected_rows["Owner"].tolist()
                    print(myusername)
                    print(mylist)
                    # tnewlist=tuple(mylist)
                    #st.write(mylist)
                    #st.write(tnewlist)
                    yesbutton=st.button("Yes",key="yes",on_click=del_task,args=(mylist,tnewlist))
def update_data_task():
    update_lic_con  = st.empty()
    
    def updatelic(id,task,ttask_detail,tbucket
                  ,ttowner,tstart_date,tdue_date,tstatus,tCompletion_stage,uploadednames,
                ttask_group,tpriority,tplan_type,tnature,ttiming,ttextent,ttactualtiming,ttactualextent,modified_by,concatenated_modified_on):
        uplic= update_task(id,task,ttask_detail,tbucket,ttowner,tstart_date,tdue_date,tstatus,tCompletion_stage,uploadednames,
                ttask_group,tpriority,tplan_type,tnature,ttiming,ttextent,ttactualtiming,ttactualextent,modified_by,concatenated_modified_on)
                #placeholder.empty()
                
        if uplic==True:
            st.toast("Record Updated Successfully...", icon="👍")
            st.session_state.selemail="------"
                        
        else:
            st.toast(f"Error:-{uplic}", icon="👎")
            st.toast("Try Again")
        
    with update_lic_con.container(border=True):
        st.subheader("Update License")
        df=get_task_list()
        if isinstance(df, pd.DataFrame):
           st.dataframe(df,hide_index=True)
        email_list = df["Id"].tolist()
        owner_list=df["Owner"].tolist()
        role_list=df["Task_Details"].tolist()
        #add item                      at beginning of list 
        email_list.insert(0,"------")
        # st.session_state.mroles="------"

        id=st.selectbox("Select ID to Update Record",options=email_list,key="selemail",placeholder="Choose as Option")
        if id !="------":
            #get data for selected email& show as default value of widgets
            # task_detail=df.loc(f"Id=={id}")["Task_Details"].item()
            task=df.query(f"Id=={id}")["Task"].item()
            task_detail=df.query(f"Id=={id}")["Task_Details"].item()
            bucket=df.query(f"Id=={id}")["Bucket"].item()
            owner=df.query(f"Id=={id}")["Owner"].item()
           
            start_date=df.query(f"Id=={id}")["Start Date"].item()
            date_str, time_str = start_date.split("_")
            print("Date:", date_str)
            print("Time:", time_str)
            due_start=df.query(f"Id=={id}")["Due Date"].item()
            due_str, due_time_str = due_start.split("_")
            print("Date:", due_str)
            print("Time:", due_time_str)
            status=df.query(f"Id=={id}")["Status"].item()
            Completion_stage=df.query(f"Id=={id}")["Completion Stage"].item()
            file=df.query(f"Id=={id}")["File"].item()
            task_group=df.query(f"Id=={id}")["Task Group"].item()
            priority=df.query(f"Id=={id}")["Priority"].item()
            plan_type=df.query(f"Id=={id}")["Plan Type"].item()
            print(plan_type)

            nature=df.query(f"Id=={id}")["Nature"].item()
            timing=df.query(f"Id=={id}")["Timing"].item()
            extent=df.query(f"Id=={id}")["Extent"].item()
            actual_timing=df.query(f"Id=={id}")["Actual Timing"].item()
            actual_extent=df.query(f"Id=={id}")["Actual Extent"].item()
            current_datetime = datetime.datetime.now()
            current_date = current_datetime.strftime("%Y-%m-%d")
            current_time = current_datetime.strftime("%H:%M")
            modified_by = st.session_state.get('Name', 'Unknown')
            concatenated_modified_on = f"{current_date}_{current_time}"
            ttask=st.text_input(f"Update Task",value=task,key="task_t")            
                  
            ttask_detail=st.text_input(f"Update Task Detail",value=task_detail,key="task_t_details")            
            tbucket=st.text_input(f"Update Bucket",value=bucket,key="task_bucket")
            owner_lists = []
#             for owner_string in owner_list:
#                 try:
#                     owner_email_list = json.loads(owner_string)
#                     if isinstance(owner_email_list, list):
#                        owner_lists.extend(owner_email_list)
#                     else:
#                        print(f"Invalid data format: {owner_string}")
#                 except json.JSONDecodeError as e:
#                        print(f"Error decoding JSON: {e}")

# # Now owner_list contains the email addresses
#             print(owner_lists)
            owner_lists = []
            for owner_string in owner_list:
    # Strip off leading and trailing characters
                owner_string = owner_string.strip("[]")

    # Split the string by comma and strip off extra spaces
                emails = [email.strip().strip('"') for email in owner_string.split(",")]

    # Extend owner_list with the extracted email addresses
                owner_lists.extend(emails)

# Now owner_list contains the email addresses
            print(owner_lists)
            ttowner = st.multiselect("Select Owner", options=owner_lists, key="task_towner", placeholder=f"Choose from")

            # ttowner=st.text_input(f"Update Towner",value=owner,key="task_towner")
            col1, col2 = st.columns(2)
            with col1:
                date_str_datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()

                start_date = st.date_input("Start Date", value=date_str_datetime,key="start_d")
                start_time= st.time_input("Start Time",value=time_obj, key="tstarttt")
                tstart_date= f"{start_date}_{start_time}"
            with col2:
                due_str_datetime = datetime.datetime.strptime(due_str, "%Y-%m-%d")
                time_due= datetime.datetime.strptime(due_time_str, "%H:%M:%S").time()

                due_date = st.date_input("Due Date",value=due_str_datetime, key="tdue_d")
                due_time = st.time_input("Due Time", value=time_due,key="tdue_due")
                tdue_date= f"{due_date}_{due_time}"
            # tstart_date=st.text_input(f"Update Start Date",value=start_date,key="task_start_date")
            # mrole=st.selectbox("Select Role to Update Record",options=role_list,key="",placeholder="Choose as Option")
            # tdue_date=st.text_input(f"Update Due Date",value=due_start,key="task_due")
            if status == "In Progress":
               status_options = ["In Progress", "Not Started", "Completed"]
               tstatus = st.selectbox("Select Status:", options=status_options, index=0, key="status_in_progress")
            elif status == "Completed":
                 status_options = ["Completed", "Not Started", "In Progress"]
                 tstatus = st.selectbox("Select Status:", options=status_options, index=0, key="status_completed")
            else:
                 status_options = ["Not Started", "In Progress", "Completed"]
                 tstatus = st.selectbox("Select Status:", options=status_options, index=0, key="status_not_started")

# Other parts of your code... 
            #    tstatus=st.text_input(f"Update Status",value=status,key="task_due_start")
            tCompletion_stage=st.number_input(f"Update Complettion Stage",value=Completion_stage,key="task_due_due")
            if file:
                st.write("Current file:", file)
            tuploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, key="file_uploader_update")
            uploadednames =file
            for uploaded_files in tuploaded_files:
                bytes_data = uploaded_files.read()
                uploadednames = uploaded_files.name
            # task=st.selectbox("Select email to Update Record",options=email_list,key="selemail",placeholder="Choose as Option")
            ttask_group=st.text_input(f"Update Task Group",value=task_group,key="task_task_group")
            # tplan_type=st.selectbox("Select email to Update Record",options=plan_type,key="selemail",placeholder="Choose as Option")
            if priority =="Low":
               priority_option = ["Low","Medium", "Critical", "High"]
               tpriority = st.selectbox("Enter The Priority", options=priority_option, index=0,key="low")
              
            elif priority == "Critical":
                 priority_option = ["Critical","Medium", "Low", "High"]
                
                 tpriority = st.selectbox("Select Status:", options=priority_option, index=0,key="critical") 
            elif priority == "High":
                 priority_option = [ "High","Medium", "Low", "Critical",]
                
                 tpriority= st.selectbox("Select Status:", options=priority_option, index=0,key="high")      
            else:  
                 priority_option = ["Medium", "Low", "Critical", "High"]
                 tpriority = st.selectbox("Select Status:", options=status_options, index=0,key="medium")  
                 
           # Initialize variables outside the if-else block
            tnature = ttiming = ttextent = ttactualtiming = ttactualextent = None

            if plan_type == "Audit Procedures":
    # Display radio button for updating plan type
               tplan_type = st.radio(f"Update Plan Type", ["Audit Procedures", "Overall Audit Plan"],horizontal=True, key="task_plan_type")
               if tplan_type == "Audit Procedures":
        # Display fields specific to "Audit Procedures"
                   if nature =="Verification":
                    
                      tnature = st.selectbox("update the Nature",("Verification", "Vouching", "Confirmation", "Reconciliation", "Analysis", "Observation", "Enquiry"))
              
                   elif nature == "Confirmation":
                        tnature = st.selectbox("update the Nature",( "Confirmation","Verification", "Vouching", "Reconciliation", "Analysis", "Observation", "Enquiry"))

                   elif nature == "Reconciliation":
                        tnature = st.selectbox("update the Nature",( "Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Observation", "Enquiry"))
                   elif nature == "Vouching":
                        tnature = st.selectbox("update the Nature",( "Vouching","Reconciliation",  "Confirmation","Verification","Analysis", "Observation", "Enquiry"))
                   elif nature == "Analysis":
                        tnature = st.selectbox("update the Nature",("Analysis", "Reconciliation",  "Confirmation","Verification", "Vouching", "Observation", "Enquiry"))
                   elif nature == "Observation":
                        tnature = st.selectbox("update the Nature",( "Observation","Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Enquiry"))
  
                   else:  
                        tnature = st.selectbox("update the Nature",( "Enquiry","Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Observation"))

                  
                   ttiming = st.text_input(f"Update Timing", value=timing, key="task_timing")
                   ttextent = st.text_input(f"Update Extent", value=extent, key="task_extent")
                   ttactualtiming = st.text_input(f"Update Actual Timing", value=actual_timing, key="task_actual_timing")
                   ttactualextent = st.text_input(f"Update Actual Extent", value=actual_extent, key="task_actual_extent")
            elif plan_type == "Overall Audit Plan":
    # Display radio button for updating plan type
                 tplan_type = st.radio(f"Update Plan Type", ["Overall Audit Plan", "Audit Procedures"],horizontal=True, key="task_plan_type")
                 if tplan_type == "Audit Procedures":
        # Display fields specific to "Audit Procedures"
                     if nature =="Verification":
                    
                      tnature = st.selectbox("update the Nature",("Verification", "Vouching", "Confirmation", "Reconciliation", "Analysis", "Observation", "Enquiry"))
              
                     elif nature == "Confirmation":
                        tnature = st.selectbox("update the Nature",( "Confirmation","Verification", "Vouching", "Reconciliation", "Analysis", "Observation", "Enquiry"))

                     elif nature == "Reconciliation":
                        tnature = st.selectbox("update the Nature",( "Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Observation", "Enquiry"))
                     elif nature == "Vouching":
                        tnature = st.selectbox("update the Nature",( "Vouching","Reconciliation",  "Confirmation","Verification","Analysis", "Observation", "Enquiry"))
                     elif nature == "Analysis":
                        tnature = st.selectbox("update the Nature",("Analysis", "Reconciliation",  "Confirmation","Verification", "Vouching", "Observation", "Enquiry"))
                     elif nature == "Observation":
                        tnature = st.selectbox("update the Nature",( "Observation","Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Enquiry"))
  
                     else:  
                        tnature = st.selectbox("update the Nature",( "Enquiry","Reconciliation",  "Confirmation","Verification", "Vouching","Analysis", "Observation"))

                  
                     ttiming = st.text_input(f"Update Timing", value=timing, key="task_timing")
                     ttextent = st.text_input(f"Update Extent", value=extent, key="task_extent")
                     ttactualtiming = st.text_input(f"Update Actual Timing", value=actual_timing, key="task_actual_timing")
                     ttactualextent = st.text_input(f"Update Actual Extent", value=actual_extent, key="task_actual_extent")

            if id>=0:
                  st.button("Update",key="upadtelic",on_click=updatelic,args=[id,ttask,ttask_detail,tbucket
                  ,ttowner,tstart_date,tdue_date,tstatus,tCompletion_stage,uploadednames,
                   ttask_group,tpriority,tplan_type,tnature,ttiming,ttextent,ttactualtiming,ttactualextent,modified_by,concatenated_modified_on])                    

# def update_data_task():
#     update_lic_con  = st.empty()
#     task=""
#     task_detail=""
#     bucket="" 
#     towner=""
#     start_date="" 
#     due_date=""
#     status=""
#     Completion_stage=""
#     uploadednames=""
#     task_group=""
#     priority="" 
#     plan_type=""
#     nature=""
#     timing=""
#     extent=""
#     tactualtiming=""
#     actualextent=""            
#     modified_by=""
#     concatenated_modified_on=""
#     def updatelic(id_lot_ext_to_check,task,ttask_detail,tbucket
#                   ,ttowner,tstart_date,tdue_date,tstatus,tCompletion_stage,uploadednames,
#                 ttask_group,tpriority,tplan_type,tnature,ttiming,ttextent,ttactualtiming,ttactualextent,modified_by,concatenated_modified_on):
#         uplic= update_task(id_lot_ext_to_check,task,ttask_detail,tbucket,ttowner,tstart_date,tdue_date,tstatus,tCompletion_stage,uploadednames,
#                 ttask_group,tpriority,tplan_type,tnature,ttiming,ttextent,ttactualtiming,ttactualextent,modified_by,concatenated_modified_on)
#                 #placeholder.empty()
                
#         if uplic==True:
#             st.toast("Record Updated Successfully...", icon="👍")
#             st.session_state.selemail="------"
                        
#         else:
#             st.toast(f"Error:-{uplic}", icon="👎")
#             st.toast("Try Again")
        
#     with update_lic_con.container(border=True):
#         st.subheader("Update License")
#         df=get_task_list()
#         if isinstance(df, pd.DataFrame):
#             st.dataframe(df,hide_index=True)
#         email_list = df["Task"].tolist()
#         role_list=df["Task_Details"].tolist()
#         #add item                      at beginning of list 
#         email_list.insert(0,"------")
#         # st.session_state.mroles="------"
#         # edited_df = st.data_editor(df, num_rows="dynamic")
#         # df = pd.DataFrame(data)
#         # df['date'] = pd.to_datetime(df['date'])

#         id_lot_ext_to_check = st.selectbox("Select ID", options=df["Id"].tolist(), index=None, placeholder="Select ID", label_visibility="collapsed")
#         filtered_df = df[df["Id"] == id_lot_ext_to_check]
#         if not filtered_df.empty:
#         # if not edited_df.empty:
#             with st.form(key="sauv_form"):
#                 edited_df = st.data_editor(filtered_df, num_rows="dynamic", use_container_width=True, hide_index=True,
#                                            column_config={
#                                                 # "Id": st.column_config.TextColumn(),
#                                                 "Task": st.column_config.TextColumn(),
#                                                 "Task_Details": st.column_config.TextColumn(),
#                                                 "Bucket": st.column_config.TextColumn(),
#                                                 "Owner": st.column_config.TextColumn(),
#                                                 "Start Date":st.column_config.TextColumn(),
#                                                 "Due Date": st.column_config.TextColumn(),
#                                                 "Status": st.column_config.TextColumn(),
#                                                 "Completion Stage": st.column_config.NumberColumn(),
#                                                 "File": st.column_config.TextColumn(),
#                                                 "Task Group": st.column_config.TextColumn(),
#                                                 "Priority": st.column_config.TextColumn(),
#                                                 "Plan Type": st.column_config.TextColumn(),
#                                                 "Nature": st.column_config.TextColumn(),
#                                                 "Timing": st.column_config.TextColumn(),
#                                                 "Extent": st.column_config.TextColumn(),
#                                                 "Actual Timing": st.column_config.TextColumn(),
#                                                 "Actual Extent": st.column_config.TextColumn()
                                             
#                                            }
#                                            )
#                 editedtask_group_dates = edited_df.loc[edited_df["Id"].idxmax()]['File']
#                 st.write("Current file:", editedtask_group_dates )
#                 uploaded_files = st.file_uploader("Choose a CSV file", type=['docx', 'xlsx', 'pdf', 'jpeg', 'png', 'jpg'], accept_multiple_files=True)
#                 uploadednames = []
#                 for uploaded_file in uploaded_files:
#                     current_datetime = datetime.datetime.now()
#                     formatted_datetime = current_datetime.strftime("%d-%m-%Y_%H-%M")
#                     name, extension = uploaded_file.name.rsplit('.', 1)
#                     file_with_timestamp = f"{name}_{formatted_datetime}.{extension}"
#                     uploadednames.append(file_with_timestamp)
#                     uploadedname = uploadednames[0] if uploadednames else st.toast("file uploaded")
                                              
             
#                 if len(task) >= 0:
#                    if st.form_submit_button("Update"):
                         
             
#                         #  st.write("Updated Task_Details values:")
#                          task =edited_df.loc[edited_df["Id"].idxmax()]["Task"]
                         
#                         #  st.write(task)
#                         #  print(task)
#                          task_detail = edited_df.loc[edited_df["Id"].idxmax()]["Task_Details"]
#                          st.write(task_detail)
#                 # Assuming these lines are meant to update the respective variables with edited values
#                          bucket = edited_df.loc[edited_df["Id"].idxmax()]["Bucket"]
#                          towner = edited_df.loc[edited_df["Id"].idxmax()]["Owner"]
#                          start_date = edited_df.loc[edited_df["Id"].idxmax()]['Start Date']
#                          due_date = edited_df.loc[edited_df["Id"].idxmax()]['Due Date']
#                          status = edited_df.loc[edited_df["Id"].idxmax()]['Status']
#                          Completion_stage = edited_df.loc[edited_df["Id"].idxmax()]['Completion Stage']
#                         #  editedtask_group_dates = edited_df['File']
#                          task_group= edited_df.loc[edited_df["Id"].idxmax()]['Task Group']
#                          priority= edited_df.loc[edited_df["Id"].idxmax()]['Priority']
#                          plan_type = edited_df.loc[edited_df["Id"].idxmax()]['Plan Type']
#                          nature= edited_df.loc[edited_df["Id"].idxmax()]['Nature']
#                          timing = edited_df.loc[edited_df["Id"].idxmax()]['Timing']
#                          extent = edited_df.loc[edited_df["Id"].idxmax()]['Extent']
#                          tactualtiming = edited_df.loc[edited_df["Id"].idxmax()]['Actual Timing']
#                          actualextent = edited_df.loc[edited_df["Id"].idxmax()]['Actual Extent']
#                          current_datetime = datetime.datetime.now()
#                          current_date = current_datetime.strftime("%Y-%m-%d")
#                          current_time = current_datetime.strftime("%H:%M")
#                          modified_by = st.session_state.get('Name', 'Unknown')
#                          concatenated_modified_on = f"{current_date}_{current_time}"
#                          print(id_lot_ext_to_check)
#                          updatelic(id_lot_ext_to_check,task, task_detail, bucket, towner, start_date, due_date, status, Completion_stage, uploadedname,
#                                   task_group, priority, plan_type, nature, timing, extent, tactualtiming, actualextent,
#                                   modified_by, concatenated_modified_on)

                
               
       
