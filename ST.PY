import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore Dashboard", page_icon=":bar_chart:", layout='wide')
st.title(":bar_chart: SuperStore Data Dashboard")

# Let us send the title up
st.markdown(""" <style>.div.block-container{padding-top: 1rem;padding-bottom: 0rem;padding-left:\
             1rem}</style>""", unsafe_allow_html=True)

# Upload the data or use the local data
# Encoding is added.
fl = st.file_uploader(":file_folder: Upload a File", type=(["csv", "txt", "xls", "xlsx"]))
if fl:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    df = pd.read_csv(r"Superstore.csv", encoding = "ISO-8859-1")

# -----------------------------------------------------------------------------
# Columns Filter by Date Range

df["Order Date"] = pd.to_datetime(df["Order Date"])
start_date = df["Order Date"].min() # The minimum data available to choose
end_date = df["Order Date"].max()   # The maximum data available to choose
middle = df["Order Date"].mean()    # The default value

col1, col2 = st.columns(2)

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", min_value = start_date, max_value = end_date, value=middle))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", min_value = start_date, max_value = end_date, value=middle + pd.DateOffset(months=6)))
# filtering Data
df = df[(df["Order Date"]>= date1) & (df["Order Date"]<= date2)].copy()

#------------------------------------------------------------------------------
# SideBar/ Filtering the Data by Region, Country, State and City
# Notice here we have hireachi of Data. First Region then States in REgion and then Cities in States.
st.sidebar.header("Choose the Filter")

# Picking Region without Limit
regions = st.sidebar.multiselect("Region", options=df["Region"].unique())
if not regions:
    df_reg = df.copy()
else:
    df_reg = df[df["Region"].isin(regions)]

# Picking states in chosen Regions
states = st.sidebar.multiselect("State", options=df_reg["State"].unique())
if not states:
    df_sta = df_reg.copy()
else:
    df_sta = df_reg[df_reg["State"].isin(states)]

# Picking the cities in chosen States.
cities = st.sidebar.multiselect("City", options=df_sta["City"].unique())
if not cities:
    df__cit = df_sta.copy()
else:
    df_cit = df_sta[df_sta["City"].isin(cities)]

#---------------------------------------------------------------------------------
# Filtering the data based on the Pickups from Sidebar

if regions and states and cities:
    df_filter = df[(df["Region"].isin(regions)) & (df["State"].isin(states)) & (df["City"].isin(cities))]
elif regions and states:
    df_filter = df[(df["Region"].isin(regions)) & (df["State"].isin(states))]
elif regions and cities:
    df_filter = df[(df["Region"].isin(regions)) & (df["City"].isin(cities))]
elif states and cities:
    df_filter = df[(df["State"].isin(states)) & (df["City"].isin(cities))]
elif regions:
    df_filter = df[df["Region"].isin(regions)]
elif states:
    df_filter = df[df["State"].isin(states)]
elif cities:
    df_filter = df[df["City"].isin(cities)]
else:
    df_filter = df.copy()

#--------------------------------------------------------------------------------------
# Plotting the Data
category_df = df_filter.groupby(by="Category", as_index=False)["Sales"].sum()

with col1:
    st.subheader("Category Wise Sale")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = [f"${i}" for i in category_df["Sales"]])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("State Wise Sale")
    fig = px.pie(df_filter, values="Sales", names="State")
    fig.update_traces(text = df_filter["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
