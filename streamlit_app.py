import streamlit as st
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



if st.button('show me your table!'):
    st.dataframe(rows)
else:
    st.write('I wont do it')

st.metric(42,2)
