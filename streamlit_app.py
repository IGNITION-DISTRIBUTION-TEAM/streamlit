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
    ctx = sf.connect(account=acc,username=user,password=passw,schema=sch,warehouse=wh,database=db)
    cs = ctx.cursor()
    st.session_state['is_ready'] = True
    return cs
    

with sidebar:
    Username1 = st.text_input("Username")
    password = st.text_input("Password")
    account = "pm58521.east-us-2.azure"
    role = "role"
    warehouse = "DISTRIBUTION_WH"
    database = "DATAWAREHOUSE"
    schema = "DISTRIBUTION_DATA_APPLICATION"
    connect = st.button("Connect to Snowflake",on_click=connect_to_snowflake, args=[account,Username1,password,schema,warehouse,database])
    


if 'is_ready' not in st.session_state:
    st.session_state ['is_ready'] = False

if st.session_state['is_ready'] == True:
    st.write("Connected")
    
