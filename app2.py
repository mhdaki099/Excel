# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Out of Stocks Report")
# uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

# if uploaded_file:
#     df = pd.read_excel(uploaded_file)

#     column_e_index = 4  
#     column_m_index = 12  


#     if column_e_index < len(df.columns) and column_m_index < len(df.columns):

#         unique_values_e = df.iloc[:, column_e_index].dropna().unique()  
#         selected_value_e = st.selectbox("Choose the Class:", unique_values_e)

#         unique_values_m = df.iloc[:, column_m_index].dropna().unique()  
#         selected_value_m = st.selectbox("Select a value from Stock Avail:", unique_values_m)

#         df_filtered = df[(df.iloc[:, column_e_index] == selected_value_e) & 
#                          (df.iloc[:, column_m_index] == selected_value_m)]

#         columns_to_display = [0, 2, 3, 13]  
#         df_filtered = df_filtered.iloc[:, columns_to_display]

#         st.write("Filtered Data Preview:")
#         st.dataframe(df_filtered)  

#         if not df_filtered.empty:
#             chart = px.bar(df_filtered, x=df_filtered.columns[0], y=df_filtered.columns[1]) 
#             st.plotly_chart(chart)
#     else:
#         st.warning("One or more required columns not found in the uploaded file.")
#         st.warning("New item was added")

import streamlit as st
import pandas as pd
import plotly.express as px

# واجهة لتحميل ملف Excel
st.title("Excel Dashboard")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # قراءة ملف Excel وتحويله إلى DataFrame
    df = pd.read_excel(uploaded_file)

    # تعريف أرقام الأعمدة
    column_a_index = 0  # العمود A
    column_d_index = 3  # العمود D
    column_n_index = 13  # العمود N
    column_o_index = 14  # العمود O
    column_m_index = 12  # العمود M (الذي يحتوي على القيم "OOS" و "Stocked")

    # التحقق من أن الأعمدة موجودة
    if (column_a_index < len(df.columns) and column_d_index < len(df.columns) and 
        column_n_index < len(df.columns) and column_o_index < len(df.columns) and column_m_index < len(df.columns)):

        # دمج محتوى الأعمدة N و O مع مسافة بينهما
        df['Remarks'] = df.iloc[:, column_n_index].astype(str) + ' ' + df.iloc[:, column_o_index].astype(str)

        # إضافة فلتر للعمود M
        unique_values_m = df.iloc[:, column_m_index].dropna().unique()
        selected_value_m = st.selectbox("Select a value from column M (Stocked/OOS):", unique_values_m)

        # تصفية البيانات بناءً على القيمة المختارة في العمود M
        df_filtered = df[df.iloc[:, column_m_index] == selected_value_m]

        # عرض البيانات مع الأعمدة المطلوبة فقط
        st.write("Filtered Data Preview:")
        st.dataframe(df_filtered[[df.columns[column_a_index], df.columns[column_d_index], 'Remarks', df.columns[column_m_index]]])

        # إنشاء المخطط الدائري (Doughnut Chart)
        df_count = df_filtered[[df.columns[column_a_index], df.columns[column_m_index]]].groupby(df.columns[column_m_index]).count().reset_index()
        df_count.columns = ['Stock Status', 'Item Count']

        if not df_count.empty:
            chart = px.pie(df_count, 
                           names='Stock Status', 
                           values='Item Count', 
                           title="Count of Items by Stock Status",
                           hole=0.4)  # لجعل المخطط دائريًا (Doughnut)
            st.plotly_chart(chart)
    else:
        st.warning("One or more required columns not found in the uploaded file.")
