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

with st.sidebar:
    option = st.selectbox('Please select a campaign',DATAUPDATE["campaignname"].unique())

st.write('You selected:', option)

rslt_df = DATAUPDATE.loc[DATAUPDATE['campaignname'] == option]

st.line_chart(rslt_df,x="date",y="totalagents")
st.line_chart(rslt_df,x="date",y="totalsales")
st.line_chart(rslt_df,x="date",y="averagescore")




    
