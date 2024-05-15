import streamlit as st
import pandas as pd
import io

# alos pip install openpyxl  
# pip install pandas_read_xml

# add excel sheets to workbook & then download the same
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}/<style>', unsafe_allow_html=True)

op = st.radio(label="Select", options=["excel", "xml"])

if op == "excel":
    th_props = [
        ('font-size', '14px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7ffff')
    ]
                               
    td_props = [
        ('font-size', '12px')
    ]
                                 
    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]
    
    buffer = io.BytesIO()
    files = ["my_data.csv", "my_data1.csv", "my_data2.csv"]
    
    with pd.ExcelWriter(buffer) as writer:
        for f in files:
            df = pd.read_csv(f)
            df.to_excel(writer, sheet_name=f)
            # st.dataframe(df)
            df2 = df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
            st.table(df2)
    st.download_button(label="Download File", data=buffer, file_name="queries.xlsx")
    buffer.flush()

else:
    st.write("xml")
    # delete &# in xml file
    st.button("show xml", key="showxml")
    # Assuming df2 is a styled DataFrame
    # styled_table_html = df2.render()
    # st.markdown(styled_table_html, unsafe_allow_html=True)
