import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from datetime import datetime
import altair as alt

url = URL(**st.secrets["snowflake"])

st.set_page_config(layout="wide")
st.title('Ignition Sales')

@st.cache_data
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

DATAUPDATE = load_data(url)

with st.sidebar:
    #option = st.selectbox('Please select a campaign',DATAUPDATE["campaignname"].unique())
    option = st.multiselect('Please select a campaign',DATAUPDATE["campaignname"].unique())
    
    DATAUPDATE = (DATAUPDATE['campaignname'].isin(option))
    
    providernames = DATAUPDATE["providername"].loc[DATAUPDATE["campaignname"] == option]
    option2 = st.selectbox('Please select a providername',providernames.unique())

    providertypes = DATAUPDATE["providertype"].loc[DATAUPDATE["campaignname"] == option]
    option3 = st.selectbox('Please select a providertype',providertypes.unique())
    
    start_date = st.date_input("Start Date", value=pd.to_datetime("2021-01-31", format="%Y-%m-%d"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
   
    mask = (DATAUPDATE['saledate'] >= start_date) & (DATAUPDATE['saledate'] <= end_date)

    df_filtered = DATAUPDATE.loc[mask]

    df_filtered = df_filtered[(DATAUPDATE['campaignname'] == option) & (df_filtered['providername'] == option2) & (df_filtered['providertype'] == option3)]

metric = df_filtered['sales'].sum()

st.metric('Sales',metric)

c = alt.Chart(df_filtered).mark_line().encode(
    x='salehour', 
    y='sum(sales)', 
    color = 'saledate:N'
    ).properties(
    width=1200,
    height=500
)

st.altair_chart(c)
