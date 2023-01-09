import toml
import streamlit as st
import pandas as pd
import snowflake.connector as sf
from datetime import date


sidebar = st.sidebar

with sidebar:
    account = st.text_input("Username")
    password = st.text_input("Password")
