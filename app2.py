import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder

# Path to save the uploaded file (you can modify this based on where you want to store the file)
file_path = "uploaded_file.xlsx"

# Function to load the file, or use the default file if not uploaded
def load_file():
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return None

# Function to save the file
def save_file(file):
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

# Login functionality for admin
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Create login UI
        st.subheader("Login")
        password = st.text_input("Enter Password", type="password")

        if st.button("Login as Admin"):
            if password == "master1234":
                st.session_state.logged_in = True
                st.session_state.page = "Admin"  # Set the page to Admin after login
                st.success("Login successful!")
            else:
                st.error("Incorrect password!")

# Admin page
def admin_page():
    st.title("Admin Page")
    
    # Show the option to keep the current file or upload a new one
    keep_current_file = st.radio("Do you want to keep the current file or upload a new one?", ["Keep Current", "Upload New"])

    if keep_current_file == "Upload New":
        uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
        if uploaded_file:
            save_file(uploaded_file)
            st.success("File uploaded successfully!")

    # Allow admin to save and view the uploaded file
    st.write("Admin options:")
    if st.button("Save"):
        df = load_file()
        if df is not None:
            st.write("Currently uploaded file:")
            st.dataframe(df)
        else:
            st.warning("No file to save or display.")

# User page
def user_page():
    st.title("Out Of Stocks Report")
    df = load_file()
    if df is not None:
        column_a_index = 0
        column_d_index = 3
        column_n_index = 13
        column_o_index = 14

        if (column_a_index < len(df.columns) and column_d_index < len(df.columns) and 
            column_n_index < len(df.columns) and column_o_index < len(df.columns)):

            # Create 'Remarks' column
            df['Remarks'] = df.iloc[:, column_n_index].astype(str) + ' ' + df.iloc[:, column_o_index].astype(str)

            item_search = st.text_input("Search for an Item Code:")
            if item_search:
                df_filtered = df[df[df.columns[column_a_index]].str.contains(item_search, case=False, na=False)]
            else:
                df_filtered = df

            st.write("Filtered Data Preview:")

            # Only select the required columns: Column A, D, and 'Remarks'
            df_filtered = df_filtered[[df.columns[column_a_index], df.columns[column_d_index], 'Remarks']]

            # Set up AgGrid with options to freeze the first column (Column A)
            gb = GridOptionsBuilder.from_dataframe(df_filtered)
            gb.configure_column(df.columns[column_a_index], pinned="left")  # Freeze the first column
            grid_options = gb.build()

            # Display the dataframe with the pinned first column using AgGrid
            AgGrid(df_filtered, gridOptions=grid_options, use_container_width=True)

        else:
            st.warning("One or more required columns not found in the uploaded file.")
    else:
        st.warning("No file uploaded yet.")

# Check if the admin is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    login()
    user_page()  # Always display user page initially
else:
    # Now check the session state for page selection
    if "page" not in st.session_state:
        st.session_state.page = "User"  # Default to User if not set
    
    # Render the selected page based on session state
    if st.session_state.page == "Admin":
        admin_page()
    else:
        user_page()
