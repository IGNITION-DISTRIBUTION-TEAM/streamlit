import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from datetime import date, timedelta
import altair as alt

current_date = datetime.today().strftime('%Y-%m-%d')+' 00:00:00'
sixmonthsago = current_date + datetime.timedelta(days=10)

url = URL(**st.secrets["snowflake"])

st.set_page_config(layout="wide")

@st.cache_data(ttl=1500)
def load_data(url):
    engine = create_engine(url)
    connection = engine.connect()    
    query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"    
    DATAUPDATE = pd.read_sql(query, connection)
    return DATAUPDATE

snowflakedata = load_data(url)


with st.sidebar:
    st.title('Ignition Sales')
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
    
current_date_mask = df_filtered.loc[(df_filtered['saledate'] == pd.Timestamp(datetime.now()))]   

col1,col2,col3,col4,col10 = st.columns(5)

with col1:
    metric = df_filtered['sales'].sum()
    st.metric('Current Sales',metric)

maxtime = df_filtered['salehour'].max()

df_average = snowflakedata[snowflakedata['campaignname'].isin(option1) & (snowflakedata['providername'] == option2) & (snowflakedata['providertype'] == option3) & (snowflakedata['saledate'] > sixmonthsago) ]
df_average = df_average.groupby(['campaignname','salehour','saledate'])['sales'].sum().reset_index()
df_average = df_average.groupby(['campaignname','salehour',])['sales'].mean().reset_index()

with col2:
    metric2 = df_average['sales'].sum()
    st.metric('Full Day Predicted Sales',round(metric2))
    
df_filtererhour =  df_average[(df_average['salehour'] <= maxtime)]

with col3:
    metric3 = sum(df_filtererhour['sales'])
    st.metric('Current Hour Predicted Sales',round(metric3))

with col4:
    metric4 = metric-metric3
    st.metric('Sales Difference',round(metric4))
    
    
if metric4 < 0:
    symbol = 'Under Predicted Target :face_with_spiral_eyes:'
else:
    symbol = 'Over Predicted Target :laughing:'
    

with col10:
    st.write(symbol)
   

col5,col6 = st.columns(2)
with col5:
    c = alt.Chart(df_filtered).mark_line().encode(
    alt.X('salehour', axis=alt.Axis(tickMinStep=1)),
    y='sum(sales)',
    color=alt.Color('saledate', legend=None)
    ).properties(
    width=800,
    height=400)
    st.altair_chart(c)

with col6:
    c = alt.Chart(df_filtered).mark_line().encode(
    alt.X('salehour', axis=alt.Axis(tickMinStep=1)),        
    y='sum(sales)', 
    color=alt.Color('campaignname', legend=None)
    ).properties(
    width=850,
    height=400)
    st.altair_chart(c)

col7,col8 = st.columns(2)

with col7:
    e = alt.Chart(df_average).mark_line().encode(
    alt.X('salehour', axis=alt.Axis(tickMinStep=1)), 
    y='sum(sales)'
    ).properties(
    width=800,
    height=400)
    st.altair_chart(e)

with col8:
    c = alt.Chart(df_average).mark_line().encode(
    alt.X('salehour', axis=alt.Axis(tickMinStep=1)),
    y='sum(sales)', 
    color=alt.Color('campaignname', legend=None)
    ).properties(
    width=850,
    height=400)
    st.altair_chart(c)
    
# col5 = st.columns(1)    
    
# with col5:
#     d = alt.Chart(df_filtered).mark_bar().encode(
#     x='campaignname:O', 
#     y='sum(sales)', 
#     color = 'campaignname:N',
#     column='saledate:N',
#     ).properties(
#     width=100,
#     height=300)
#     st.altair_chart(d)    
