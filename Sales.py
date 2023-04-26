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
    providernames = DATAUPDATE["providername"].loc[DATAUPDATE["campaignname"] == option]
    option2 = st.selectbox('Please select a providername',providernames.unique())

    providertypes = DATAUPDATE["providertype"].loc[DATAUPDATE["campaignname"] == option]
    option3 = st.selectbox('Please select a providertype',providertypes.unique())
    
    
rslt_df1 = DATAUPDATE.loc[DATAUPDATE['campaignname'] == option]
rslt_df2 = rslt_df1.loc[DATAUPDATE['providername'] == option2]
rslt_df3 = rslt_d3.loc[DATAUPDATE['providertype'] == option3]

st.subheader('Total Agents ')
st.line_chart(rslt_df3,x="saledate",y="sales")
