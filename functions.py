import sqlite3
import random
import string
import smtplib
import pandas as pd
import streamlit as st
import os.path
import pickle
from datetime import date,timedelta
from datetime import datetime
import numpy as np
from os.path import join, dirname, abspath
import smtplib
import ssl
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string

#db_path = join0(dirname(dirname(abspath(__file__))), 'autoaudit.db')
db_path='taskmanagement.db'
def send_email(sender_email, receiver_email, subject, body, password):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach body to the email
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
    except Exception as e:
        st.error(f"Error sending email: {e}")
def generate_otp():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))    
def send_email_notification(receiver_email,names,passwords):
    # print(names);
    # print(passwords);
    sender_email = "gauravpatil290198@gmail.com"  # Your email address
    password = "kcxqtnnxxqgohuqq"  # Your email password
    subject = "License Added Notification"
    body = body = f"""
    <html>
      <head></head>
      <body>
         <p>Welcome<span  style="color: blue;font-weight: bold;">{names},</span></p>
        <p>Your password is:<span  style="color: blue;font-weight: bold;"> {passwords}</span></p>
      </body>
    </html>
    """

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach body to the email
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.toast("Email sent successfully! 🚀", icon="👍")
       
        print('Email notification sent successfully! 🚀')
    except Exception as e:
        print(f"Error sending email notification: {e}")

# Example usage
# receiver_email = "recipient_email@example.com"
def update_password(confirm_password, email_receiver):
    try:
        print(confirm_password,email_receiver);
         # Replace with your actual database path
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query=f"UPDATE Users SET  Password ='{confirm_password}' WHERE `Username` = '{email_receiver}'"
        #query=f"SELECT Review from Audit_AR where DataSetName='{DsName}' AND CompanyName='{comp_name}'"
        #st.write(query)
        cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()
      
        print("Password updated successfully!")
        
    except sqlite3.Error as error:
        print("SQLite error:", error)
        # Handle the error appropriately, e.g., log it or raise an exception
        
    except Exception as e:
        print("Runtime error:", e)
        # Handle other exceptions, e.g., log them or display an error message
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite connection closed.")

def get_user_rights():
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query="SELECT * from Users_Rights"
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
    return userrights

def check_login(Username, password):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()

        # Execute the query to retrieve user information
        cursor.execute(f"SELECT Id, Username, Password, Role, Name FROM Users WHERE Username='{Username}' AND Is_deleted='false'")
        passworddb = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        sqliteConnection.close()
        print(passworddb)           
        if passworddb:
            # If the user exists, check if the password matches
            st.session_state['loggedIn'] = True
            st.session_state['Username'] = passworddb[1]
            st.session_state['Role'] = passworddb[3]  # Role
            st.session_state['Name'] = passworddb[4]  # Name
            print(st.session_state['Role'])
            print(st.session_state['Name'])
            print(st.session_state['Username'])
            # Display user information
            return True
        else:
            st.toast("Invalid password")
            return False 
    except sqlite3.Error as error:
        if sqliteConnection:
            sqliteConnection.close()
        st.toast(f"Error: {error}")
        return False
    except Exception as e:
        st.toast("An error occurred during login.")
        return False


    except sqlite3.Error as error:
        if sqliteConnection:
            sqliteConnection.close()
        st.toast(f"Error: {error}")
        return False

    except Exception as e:
        st.toast("An error occurred during login.")
        return False


# Uncomment and properly place this code snippet within your Streamlit application
# if len(password) > 0 and len(userName) > 1:
#     st.button("Login", on_click=check_login, args=(userName, password,))


def add_new_license(Username, Password, role, Name):
    sqliteConnection = None
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        
        # Define the SQL query
        sqlite_insert_with_param = """INSERT INTO Users (Username, Password, Role, Name) VALUES (?, ?, ?, ?);"""
        
        # Specify the data to be inserted
        data_tuple = (Username, Password, role, Name)
        
        # Execute the SQL query
        cursor.execute(sqlite_insert_with_param, data_tuple)
        
        # Commit the transaction
        sqliteConnection.commit()
        
        return True
    
    except sqlite3.Error as error:
        # Handle SQLite errors
        return error
    
    except Exception as e:
        # Handle other exceptions
        return e
    
    finally:
        # Close the database connection
        if sqliteConnection:
            sqliteConnection.close()

def get_licen():
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query = "SELECT * FROM Users WHERE Is_deleted = 'false'"  # Assuming 'Is_deleted' is a string column
        sql_query = pd.read_sql_query(query, sqliteConnection)
        return sql_query
    except Exception as e:
        return e
    finally:
        if 'sqliteConnection' in locals():
            if sqliteConnection:
                sqliteConnection.close()
                # message=("The SQLite connection is closed")
def update_users(Username,Role,Name):

    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        #update audit status
        query = f"UPDATE Users SET Role = '{Role}', Name = '{Name}' WHERE Username = '{Username}'"
        #query=f"SELECT Review from Audit_AR where DataSetName='{DsName}' AND CompanyName='{comp_name}'"
        #st.write(query)
        cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        return error
    except Exception as e:
        return e 
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #message=("The SQLite connection is closed")

def del_lic(mylistid, username):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print(mylistid[0])
        print(username[0])
        ud = "d" 
        concatenated_username = f"{mylistid[0]}_{username[0]}_{ud}"
        if len(mylistid) > 1:
            # Update the Username and Is_deleted fields in the Users table
            cursor.execute("UPDATE Users SET Username = ?, Is_deleted = ? WHERE Id = ?", (concatenated_username, 'True', mylistid[0]))
        else:
           cursor.execute("UPDATE Users SET Username = ?, Is_deleted = ? WHERE Id = ?", (concatenated_username, 'True', mylistid[0]))        
            
        sqliteConnection.commit()
        cursor.close()
        st.toast(f'Records Deleted...')
        return True
    except sqlite3.Error as error:
        st.toast(f'{error}')
        return error
    except Exception as e:
        st.toast(f'{e}')
        return e 
    finally:
        if sqliteConnection:
            sqliteConnection.close()

