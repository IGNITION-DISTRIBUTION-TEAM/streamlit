import streamlit as st
from streamlit_extras.let_it_rain import rain
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from datetime import datetime
import altair as alt

current_date = datetime.today().strftime('%Y-%m-%d')+' 00:00:00'

url = URL(**st.secrets["snowflake"])

st.set_page_config(layout="wide",page_title="Documentation", page_icon="🌍")

@st.cache_data(ttl=1500)
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION.TM_CAMPAIGN_DOCUMENTATION"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

snowflakedata = load_data(url)

st.dataframe(snowflakedata, use_container_width=True)

with st.sidebar:
        snowflakedata = snowflakedata.sort_values(by=['CAMPAIGN_NAME'])
        option1 = st.selectbox('Please select a Campaign Name',snowflakedata.unique())
