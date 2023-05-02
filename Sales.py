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

@st.cache_data(ttl=3600)
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

DATAUPDATE = load_data(url)

with st.sidebar:
    DATAUPDATE = DATAUPDATE.sort_values(by=['campaignname'])
    option1 = st.multiselect('Please select a campaign',DATAUPDATE["campaignname"].unique())
    
    providernames = DATAUPDATE["providername"].loc[DATAUPDATE['campaignname'].isin(option1)]
    option2 = st.selectbox('Please select a providername',providernames.unique())

    providertypes = DATAUPDATE["providertype"].loc[DATAUPDATE['campaignname'].isin(option1) & DATAUPDATE['providername'].isin(providernames)]
    option3 = st.selectbox('Please select a providertype',providertypes.unique())
    
    start_date = st.date_input("Start Date", value=pd.to_datetime("2021-01-31", format="%Y-%m-%d"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
    
    df_filtered = DATAUPDATE[DATAUPDATE['campaignname'].isin(option1) & (DATAUPDATE['providername'] == option2) & (DATAUPDATE['providertype'] == option3)]
    mask = (df_filtered['saledate'] >= start_date) & (df_filtered['saledate'] <= end_date)
    df_filtered = df_filtered.loc[mask]  

metric = df_filtered['sales'].sum()

st.metric('Sales',metric)

col1, col2= st.columns(2)

with col1:
    c = alt.Chart(df_filtered).mark_line().encode(
    x='salehour', 
    y='sum(sales)', 
    color = 'saledate:N'
    ).properties(
    width=1200,
    height=500)
    st.altair_chart(c)



d = alt.Chart(df_filtered).mark_bar().encode(
    x='campaignname:O', 
    y='sum(sales)', 
    color = 'campaignname:N',
    column='saledate:N'
    ).properties(
    width=100,
    height=500)

st.altair_chart(d)
