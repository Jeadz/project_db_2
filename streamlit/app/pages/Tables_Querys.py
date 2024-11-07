import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/"

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
            
            response = requests.post(f"{API_BASE_URL}tables", json=new_table)
            
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
            response = requests.post(f"{API_BASE_URL}tables/upload_excel_tables/", files=files)
            
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(f"Error: {response.json().get('detail', 'An error has occurred')}")
                
create_tables()
create_tables_bulk()