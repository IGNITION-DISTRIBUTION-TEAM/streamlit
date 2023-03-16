import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector

# Initialize connection.
# Uses st.cache_resource to only run once.


st.title('Onair Campaign Stats')

def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    


rows = run_query("select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.TM_AD_ONAIR_PERFORMANCE_STATS")    


for row in rows:
    st.dataframe(rows[1])



    
# st.line_chart(rows,7,5)
