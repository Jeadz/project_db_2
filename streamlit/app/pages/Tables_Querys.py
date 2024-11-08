import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/tables/"

def create_tables():
    st.subheader("Create Table:")
    with st.form(key='table_form'):
        table_number = st.text_input("Table Number: ")
        capacity = st.text_input("Table Capacity: ")
        
        submit = st.form_submit_button("Create Table")
        
        if submit:
            new_table = {
                "table_number": table_number,
                "capacity": capacity
            }
            
            response = requests.post(f"{API_BASE_URL}", json=new_table)
            
            if response.status_code in [200,201]:
                st.success('Table Create Successfully')
            else:
                st.error(f'Error While Tried Create A Table: {response.status_code} - {response.text}')
                
def create_tables_bulk():
    st.subheader("Load Bulk Tables")
    uploaded_file = st.file_uploader("Load Excel File", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        file_name = uploaded_file.name  
        
        if st.button("Send To FastAPI"):
            files = { 
                "file": (file_name, uploaded_file.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            }
            response = requests.post(f"{API_BASE_URL}upload_excel_tables/", files=files)
            
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.json().get('detail', 'An error has occurred')}")
                
                
def update_table():
    st.subheader("Update Table")
    table_id = st.text_input("Table ID to Update: ")
    
    table_number = st.text_input("New Number for the Table: ")
    capacity = st.text_input("New Capacity for the Table: ")
    
    if st.button("Update Table"):
        if table_id.isdigit():
            table_id = int(table_id)
            table_data = {}
            if table_number:
                table_data["table_number"] = table_number
            if capacity:
                table_data["capacity"] = capacity
            
            if table_data:
                response = requests.put(f'{API_BASE_URL}update_table/{table_id}', json=table_data)
                
                if response.status_code == 200:
                    st.success('Table Updated Successfully')
                elif response.status_code == 404:
                    st.error("Table Not Found")
                else:
                    st.error(f'Error While Tried Update A Table: {response.json().get('detail')}')
            
            else:
                st.error("You must provide at least one field to update.")
        else:
            st.warning("Please, enter a valid Table ID")

def delete_table_by_id():
    st.subheader("Delete Table By ID")
    table_id = st.text_input("Table ID: ")
    if st.button("Delete Table"):
        response = requests.delete(f"{API_BASE_URL}delete_table/{table_id}")
        
        if response.status_code == 200:
            st.success(response.json().get("message"))
        elif response.status_code == 404:
            st.error("Table Not Found")
        else:
            st.error("ERROR Trying Delete Table")
    else:
        st.warning("Please, Input a valid Table ID")
    
    
    
    
    
create_tables()
create_tables_bulk()
update_table()
delete_table_by_id()