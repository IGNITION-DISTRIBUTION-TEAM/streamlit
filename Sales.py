import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

st.set_page_config(layout="wide")
st.title('Ignition Sales')





