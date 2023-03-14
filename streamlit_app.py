import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector

# Initialize connection.
# Uses st.cache_resource to only run once.



def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

st.title('How to look at table data')

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from TM_API_SCHEDULETYPES;")


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

    

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('show me your table!'):
        st.dataframe(rows)
    else:
        st.write('I wont do it')

with col2:
    st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")    
