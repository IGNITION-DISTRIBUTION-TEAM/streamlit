import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from datetime import datetime
import altair as alt

current_date = datetime.today().strftime('%Y-%m-%d')+' 00:00:00'

url = URL(**st.secrets["snowflake"])

st.set_page_config(layout="wide")
st.title('Ignition Sales')

@st.cache_data(ttl=1500)
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

snowflakedata = load_data(url)
# snowflakedata['saledate'] = pd.to_datetime(snowflakedata['saledate'], format='%Y-%m-%d')

# current_date_mask = snowflakedata[(snowflakedata['saledate'] == current_date)]
# current_date_mask = snowflakedata.loc[(snowflakedata['saledate'] == current_date)]

current_date_mask = snowflakedata.loc[snowflakedata['saledate'] == pd.Timestamp(datetime.now()), 'saledate'].to_frame()

st.write(current_date)
st.dataframe(current_date_mask)
st.dataframe(snowflakedata)

with st.sidebar:
    snowflakedata = snowflakedata.sort_values(by=['campaignname'])
    option1 = st.multiselect('Please select a campaign',snowflakedata["campaignname"].unique())
    
    providernames = snowflakedata["providername"].loc[snowflakedata['campaignname'].isin(option1)]
    option2 = st.selectbox('Please select a providername',providernames.unique())

    providertypes = snowflakedata["providertype"].loc[snowflakedata['campaignname'].isin(option1) & snowflakedata['providername'].isin(providernames)]
    option3 = st.selectbox('Please select a providertype',providertypes.unique())
    
    start_date = st.date_input("Start Date", value=pd.to_datetime("2021-01-31", format="%Y-%m-%d"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
    
    df_filtered = snowflakedata[snowflakedata['campaignname'].isin(option1) & (snowflakedata['providername'] == option2) & (snowflakedata['providertype'] == option3)]
    mask = (df_filtered['saledate'] >= start_date) & (df_filtered['saledate'] <= end_date)
    df_filtered = df_filtered.loc[mask]  

metric = df_filtered['sales'].sum()
st.metric('Sales',metric)
col1,col2 = st.columns(2)

with col1:
    c = alt.Chart(df_filtered).mark_line().encode(
    x='salehour', 
    y='sum(sales)', 
    color = 'saledate:N'
    ).properties(
    width=1200,
    height=500)
    st.altair_chart(c)

with col2:
    c = alt.Chart(df_filtered).mark_line().encode(
    x='salehour', 
    y='sum(sales)', 
    color = 'campaignname:N'
    ).properties(
    width=1200,
    height=500)
    st.altair_chart(c)
    
col3,col4 = st.columns(2)

with col3:
    d = alt.Chart(df_filtered).mark_bar().encode(
    x='campaignname:O', 
    y='sum(sales)', 
    color = 'campaignname:N',
    column='saledate:N',
    ).properties(
    width=100,
    height=300)
    st.altair_chart(d)

df_average = snowflakedata[snowflakedata['campaignname'].isin(option1) & (snowflakedata['providername'] == option2) & (snowflakedata['providertype'] == option3)]
df_average = df_average.groupby(['campaignname','salehour','saledate'])['sales'].sum().reset_index()
df_average = df_average.groupby(['campaignname','salehour',])['sales'].mean().reset_index()

with col4:
    e = alt.Chart(df_average).mark_line().encode(
    x='salehour', 
    y='sum(sales)', 
    color = 'campaignname:N'
    ).properties(
    width=1200,
    height=500)
    st.altair_chart(e)
