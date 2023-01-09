import toml
import streamlit as st
import pandas as pd
import snowflake.connector as sf
from datetime import date

sidebar = st.sidebar



#mainuser = "SVC_DISTRIBUTION_DATA"
#mainpassword = "khrKV3ymWLvMg6QczKMr!!"

mainschema = "DISTRIBUTION_DATA_APPLICATION"

def  connect_to_snowflake(acc,user,passw,sch,wh,db):
    ctx = sf.connect(account=acc,user=user,password=passw,schema=sch,warehouse=wh,database=db)
    cs = ctx.cursor()
    # keep connection in memery
    st.session_state['Snow_conn'] = cs
    st.session_state['is_ready'] = True
    return cs

def get_data():
    query = 'select 1'
    results = st.session_state['Snow_conn'].execute(query)
    results = st.session_state['Snow_conn'].fetch_pandas_all()
    return results

with sidebar:
    Username = st.text_input("Username")
    password = st.text_input("Password")
    account = "pm58521.east-us-2.azure"
    role = "role"
    warehouse = "DISTRIBUTION_WH"
    database = "DATAWAREHOUSE"
    schema = "DISTRIBUTION_DATA_APPLICATION"
    connect = st.button("Connect to Snowflake",on_click=connect_to_snowflake, args=[account,Username,password,schema,warehouse,database])
    


if 'is_ready' not in st.session_state:
    st.session_state ['is_ready'] = False

if st.session_state['is_ready'] == True:
    st.write("Connected")
    data = get_data()
    st.dataframe(data)
