import streamlit as st
import requests
 
API_BASE_URL = "http://localhost:8000/users/" 

def create_user():
    st.subheader("Create User:")
    with st.form(key='user_form'):
        fullname = st.text_input("User full name")
        email = st.text_input("User email")
        
        submit = st.form_submit_button("Create User")
        
        if submit:
            new_user = {
                "fullname": fullname,
                "email": email
            }
        
            response = requests.post(f"{API_BASE_URL}", json=new_user)
            
            if response.status_code in [200, 201]:
                st.success('User Create Successfully')
            else:
                st.error(f"Error While Tried Create An User: {response.status_code} - {response.text}")

def create_user_bulk():
    st.subheader("Load Bulk Users")
    uploaded_file = st.file_uploader("Load Excel File", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        file_name = uploaded_file.name  
        
        if st.button("Send To FastAPI"):
            files = { 
                "file": (file_name, uploaded_file.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            }
            response = requests.post(f"{API_BASE_URL}upload_excel/", files=files)
            
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.json().get('detail', 'An error has occurred')}")

def update_user():
    st.subheader("Update User")
    user_id = st.text_input("User ID to Update: ")
    
    fullname = st.text_input("New User Name")
    email = st.text_input("New User Email")

    if st.button("Update User"):
        if user_id.isdigit(): 
            user_id = int(user_id)
            user_data = {}
            if fullname:
                user_data["fullname"] = fullname
            if email:
                user_data["email"] = email
            
            if user_data:
                response = requests.put(f'{API_BASE_URL}update_user/{user_id}', json=user_data)
                
                if response.status_code == 200:
                    st.success("User Update Successfully.")
                elif response.status_code == 404:
                    st.error("User Not Found")
                else:
                    st.error(f"Error While Tried Update A User: {response.json().get('detail')}")
            else:
                st.warning("You must provide at least one field to update.")
                
        else:
            st.warning("Please, enter a valid user ID")


def delete_user_by_id():
    st.subheader("Delete User By ID")
    user_id = st.text_input("User ID To Delete")
    if st.button("Delete User"):
        if user_id:
            response = requests.delete(f"{API_BASE_URL}user_delete/{user_id}")
            
            if response.status_code == 200:
                st.success(response.json().get("message"))
            elif response.status_code == 404:
                st.error("User Not Found")
            else:
                st.error("ERROR Trying User Delete")
        else:
            st.warning("Please, Input A Valid User ID")
        
def consult_all_users():
    st.subheader("List All Users")
    if st.button("Show All Users"):
        response = requests.get(f"{API_BASE_URL}")
        if response.status_code == 200:
            users = response.json()
            st.write("Users:", users)
        else:
            st.error(f"Error to search the users: {response.status_code} - {response.text}")

def consult_user_by_id():
    st.subheader("Search User By ID")
    user_id = st.number_input("User ID", min_value=1)
    if st.button("Search User"):
        response = requests.get(f"{API_BASE_URL}{user_id}")
        if response.status_code == 200:
            user = response.json()
            if user:
                st.write("User Found:", user)
            else:
                st.warning("User No Found")
        else:
            st.error(f"Error to search the user ID: {response.status_code} - {response.text}")



create_user()
create_user_bulk()
update_user()
delete_user_by_id()
consult_user_by_id()
consult_all_users()
