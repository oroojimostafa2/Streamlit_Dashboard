import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore Dashboard", page_icon=":bar_chart:", layout='wide')
st.title(":bar_chart: SuperStore Data")