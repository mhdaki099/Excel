import streamlit as st
import pandas as pd
import os

file_path = "uploaded_file.xlsx"

def load_file():
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return None

def save_file(file):
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.subheader("Login")
        password = st.text_input("Enter Password", type="password")

        if st.button("Login as Admin"):
            if password == "master1234":
                st.session_state.logged_in = True
                st.session_state.page = "Admin"  
                st.success("Login successful!")
            else:
                st.error("Incorrect password!")

def admin_page():
    st.title("Admin Page")
    
    keep_current_file = st.radio("Do you want to keep the current file or upload a new one?", ["Keep Current", "Upload New"])

    if keep_current_file == "Upload New":
        uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
        if uploaded_file:
            save_file(uploaded_file)
            st.success("File uploaded successfully!")

    st.write("Admin options:")
    if st.button("Save"):
        df = load_file()
        if df is not None:
            st.write("Currently uploaded file:")
            st.dataframe(df)
        else:
            st.warning("No file to save or display.")


def user_page():
    st.title("Out Of Stocks Report")
    df = load_file()
    if df is not None:
        column_a_index = 0
        column_d_index = 3
        column_e_index = 4 
        column_m_index = 12 
        column_n_index = 13
        column_o_index = 14

        if (column_a_index < len(df.columns) and column_d_index < len(df.columns) and 
            column_e_index < len(df.columns) and column_m_index < len(df.columns) and 
            column_n_index < len(df.columns) and column_o_index < len(df.columns)):

            df['Remarks'] = df.iloc[:, column_n_index].astype(str) + ' ' + df.iloc[:, column_o_index].astype(str)

            df_filtered = df[
                ((df[df.columns[column_e_index]] == "A") | (df[df.columns[column_e_index]] == "B")) &
                (df[df.columns[column_m_index]] == "OOS")
            ]

            st.write("Filtered Data Preview:")
            hide_table_row_index = """
                    <style>
                    .streamlit-expanderHeader, .css-1h6uug3, .css-1d391kg, .css-10trblm {
                        display: none;
                    }
                    .css-1v3fvcr {
                        overflow-x: auto;
                    }
                    .css-1v3fvcr table {
                        width: 100%;
                        table-layout: fixed;
                    }
                    </style>
                    """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)

            st.dataframe(df_filtered[[df.columns[column_a_index], df.columns[column_d_index], df.columns[column_e_index], 'Remarks']], use_container_width=True)

        else:
            st.warning("One or more required columns not found in the uploaded file.")
    else:
        st.warning("No file uploaded yet.")


if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    login()
    user_page()  
else:
    if "page" not in st.session_state:
        st.session_state.page = "User"  
    if st.session_state.page == "Admin":
        admin_page()
    else:
        user_page()
