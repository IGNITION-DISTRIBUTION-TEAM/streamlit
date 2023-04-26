import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

st.set_page_config(layout="wide")
st.title('Ignition Sales')

url = URL(**st.secrets["snowflake"])

engine = create_engine(url)
connection = engine.connect()

query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"

DATAUPDATE = pd.read_sql(query, connection)


with st.sidebar:
    option = st.selectbox('Please select a campaign',DATAUPDATE["campaignname"].unique())
    option2 = st.selectbox('Please select a providername',DATAUPDATE["providername"].unique())

st.dataframe(option)
