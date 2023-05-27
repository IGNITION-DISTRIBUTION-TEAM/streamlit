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

# url = URL(**st.secrets["snowflake"])

st.set_page_config(layout="wide",page_title="IG Sales", page_icon="🌍",    initial_sidebar_state="expanded",    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

# @st.cache_data(ttl=1500)
# def load_data(url):
#     engine = create_engine(url)
#     connection = engine.connect()    
#     query = "select * from DATAWAREHOUSE.DISTRIBUTION_DATA_APPLICATION.VW_AD_SALES_UPDATED"    
#     DATAUPDATE = pd.read_sql(query, connection)
#     return DATAUPDATE

# snowflakedata = load_data(url)
