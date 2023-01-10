from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Environment Data Atlas",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
)

# Create Session object
def create_session_object():
    connection_parameters = {
      "account": "pm58521.east-us-2.azure",
      "user": "SVC_DISTRIBUTION_DATA",
      "password": "khrKV3ymWLvMg6QczKMr!!",
      "warehouse": "DISTRIBUTION_WH",
      "database": "DATAWAREHOUSE",
      "schema": "DISTRIBUTION_DATA_APPLICATION"
    }
    session = Session.builder.configs(connection_parameters).create()
    print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
    return session

# Add header and a subheader
st.header("Knoema: Environment Data Atlas")
st.subheader("Powered by Snowpark for Python and Snowflake Data Marketplace | Made with Streamlit")
  
# Create Snowpark DataFrames that loads data from Knoema: Environmental Data Atlas
def load_data(session):
    # CO2 Emissions by Country
    snow_df_co2 = session.table("TW_SAC_SALES_ALL_CAMPAIGNS")
    
    # Convert Snowpark DataFrames to Pandas DataFrames for Streamlit
    pd_df_co2  = snow_df_co2.to_pandas()
    
    with st.container():
            st.dataframe(pd_df_co2)
    
if __name__ == "__main__":
    session = create_session_object()
    load_data(session)
