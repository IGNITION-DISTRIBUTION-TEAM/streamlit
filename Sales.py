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

min_date = datetime.datetime(2020,1,1)
max_date = datetime.date(2022,1,1)

a_date = st.date_input("Pick a date", min_value=min_date, max_value=max_date)


with st.sidebar:
    option = st.selectbox('Please select a campaign',DATAUPDATE["campaignname"].unique())
    providernames = DATAUPDATE["providername"].loc[DATAUPDATE["campaignname"] == option]
    option2 = st.selectbox('Please select a providername',providernames.unique())

    providertypes = DATAUPDATE["providertype"].loc[DATAUPDATE["campaignname"] == option]
    option3 = st.selectbox('Please select a providertype',providertypes.unique())
    
    start_date = st.date_input("Start Date", value=pd.to_datetime("2021-01-31", format="%Y-%m-%d"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))

# convert the dates to string
start = start_date.strftime("%Y-%m-%d")
end = end_date.strftime("%Y-%m-%d")

st.table(Series.loc[start:end]
    
    
df_filtered = DATAUPDATE[(DATAUPDATE['campaignname'] == option) & (DATAUPDATE['providername'] == option2) & (DATAUPDATE['providertype'] == option3)]

st.subheader('Total Agents ')
st.line_chart(df_filtered,x="saledate",y="sales")
