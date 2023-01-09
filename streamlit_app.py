import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
from snowflake.snowpark import Session

mainaccount = "pm58521.east-us-2.azure"
mainuser = "SVC_DISTRIBUTION_DATA"
mainpassword = "khrKV3ymWLvMg6QczKMr!!"
mainwarehouse = "DISTRIBUTION_WH"
maindatabase = "DATAWAREHOUSE"
mainschema = "DISTRIBUTION_DATA_APPLICATION"
SProcedure = "SP_DMASA_AUTOMATION"

connection_parameters = { "account": mainaccount,
                         "user": mainuser,
                         "password": mainpassword,
                         "warehouse": mainwarehouse,
                         "database": maindatabase,
                         "schema": mainschema} 


new_session = Session.builder.configs(connection_parameters).create()  

procedureruninfo = new_session.call(SProcedure) 

viewdata = Session.table(new_session,"VW_SALES_ALL_CAMPAIGNS").collect()

snowflake_df = Session.create_dataframe(new_session,viewdata)
pandas_df = snowflake_df.to_pandas()

new_session.close()

st.line_chart(pandas_df)
