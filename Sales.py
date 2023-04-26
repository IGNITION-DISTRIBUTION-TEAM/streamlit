import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

# Initialize connection.
# Uses st.cache_resource to only run once.

st.set_page_config(layout="wide")

url = URL(**st.secrets["snowflake"])

engine = create_engine(url)
connection = engine.connect()

query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.TM_AD_ONAIR_PERFORMANCE_STATS"

DATAUPDATE = pd.read_sql(query, connection)


st.title('Onair Campaign Stats')

# with st.sidebar:
#     option = st.selectbox('Please select a campaign',DATAUPDATE["campaignname"].unique())
    
# st.sidebar.success("Select a demo above.")    

# st.write('You selected:', option)

# rslt_df = DATAUPDATE.loc[DATAUPDATE['campaignname'] == option]

# col1, col2, col3 = st.columns(3)

# with col1:
#    st.subheader('Total Agents ')
#    st.line_chart(rslt_df,x="date",y="totalagents")

# with col2:
#    st.subheader('Total Sales')
#    st.line_chart(rslt_df,x="date",y="totalsales")

# with col3:
#    st.subheader('Average Score')
#    st.line_chart(rslt_df,x="date",y="averagescore")

# col4, col5, col6 = st.columns(3)

with col4:
   st.subheader('Sales Rate')
   st.line_chart(rslt_df,x="date",y="salesrate")

with col5:
   st.subheader('Contact conversion')
   st.line_chart(rslt_df,x="date",y="contact_conversion")

with col6:
   st.subheader('RPC conversion')
   st.line_chart(rslt_df,x="date",y="rpc_conversion")
