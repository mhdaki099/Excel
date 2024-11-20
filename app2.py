import streamlit as st
import pandas as pd

st.title("Out Of Stocks Report")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    column_a_index = 0
    column_d_index = 3
    column_n_index = 13
    column_o_index = 14

    if (column_a_index < len(df.columns) and column_d_index < len(df.columns) and 
        column_n_index < len(df.columns) and column_o_index < len(df.columns)):

        df['Remarks'] = df.iloc[:, column_n_index].astype(str) + ' ' + df.iloc[:, column_o_index].astype(str)

        item_search = st.text_input("Search for an Item Code:")
        if item_search:
            df_filtered = df[df[df.columns[column_a_index]].str.contains(item_search, case=False, na=False)]
        else:
            df_filtered = df

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

        st.dataframe(df_filtered[[df.columns[column_a_index], df.columns[column_d_index], 'Remarks']], use_container_width=True)

    else:
        st.warning("One or more required columns not found in the uploaded file.")
