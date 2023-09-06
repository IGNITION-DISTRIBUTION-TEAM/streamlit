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
st.set_page_config(layout="wide",page_title="IG Sales", page_icon="🌍")

@st.cache_data(ttl=3500)
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.TR_DIALLER_LEAD_COUNTS"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

snowflakedata = load_data(url)

with st.sidebar:
    st.title('Ignition Sales')
    snowflakedata = snowflakedata.sort_values(by=['campaignname'])
    option1 = st.multiselect('Please select a campaign',snowflakedata["campaignname"].unique())
    
    start_date = st.date_input("Start Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
    
    df_filtered = snowflakedata[snowflakedata['campaignname'].isin(option1)]
    mask = (df_filtered['datedialled'] >= start_date) & (df_filtered['datedialled'] <= end_date)
    df_filtered = df_filtered.loc[mask]  

st.title(option1)
st.dataframe(df_filtered)
