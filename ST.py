import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore Dashboard", page_icon=":bar_chart:", layout='wide')
st.title(":bar_chart: SuperStore Data Dashboard")

# Let us send the title up
st.markdown(""" <style>.block-container{padding-top: 2rem;padding-bottom: 0rem;padding-left:\
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
    fig = px.pie(df_filter, values="Sales", names="City")
    fig.update_traces(text = df_filter["City"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

#----------------------------------------------------------------------------------------
# Downloading the data of the graphs

cl1, cl2 = st.columns(2)

with cl1:
    with st.expander("Category Wise Sale Data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Category Wise Data.csv", mime="text/csv")

with cl2:
    with st.expander("City Wise Sale Data"):
        city_df = df_filter.groupby(by="City", as_index=False)["Sales"].sum()
        st.write(city_df.style.background_gradient(cmap="Oranges"))
        csv = city_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="City Wise Sale Data.csv", mime="text/csv")

#-------------------------------------------------------------------------------------------------------------
# Now Time versus Sale Analysis
df_filter["month-year"] = df_filter["Order Date"].dt.to_period("M")
df_filter["month-year"] = df_filter["month-year"] .dt.strftime("%Y : %b")
st.subheader("Sale/ Time Analysis")
linechart = pd.DataFrame(df_filter.groupby(by="month-year", as_index=False)["Sales"].sum())
fig = px.line(linechart, x = "month-year", y="Sales")
st.plotly_chart(fig, use_container_width=True)

with st.expander("Time Series Data"):
    st.write(linechart.T.style.background_gradient(cmap="Reds"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv, file_name="Time_Sales.csv")
