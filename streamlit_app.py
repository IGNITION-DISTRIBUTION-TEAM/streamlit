import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

# Initialize connection.
# Uses st.cache_resource to only run once.

url = URL(**st.secrets["snowflake"])

engine = create_engine(url)
connection = engine.connect()

query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.TM_AD_ONAIR_PERFORMANCE_STATS"

DATAUPDATE = pd.read_sql(query, connection)

st.title('Onair Campaign Stats')

option = st.selectbox(
    'Please select a campaign',DATAUPDATE["campaignname"].unique())

st.write('You selected:', option)

rslt_df = DATAUPDATE.loc[DATAUPDATE['campaignname'] == option]

st.dataframe(rslt_df)

st.line_chart(rslt_df,x="date",y=("totalagents","tatalsales"))





# def init_connection():
#     return snowflake.connector.connect(
#         **st.secrets["snowflake"], client_session_keep_alive=True
#     )

# conn = init_connection()

# # Perform query.
# # Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()
    


# rows = run_query("select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.TM_AD_ONAIR_PERFORMANCE_STATS")    

# df = pd.DataFrame(rows)
# st.table(rows.iloc[0:10])
    
