import streamlit as st
import requests
import pandas as pd

resp = requests.get('https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json')
json = resp.json()
codes, emojis = zip(*json.items())
df = pd.DataFrame({'Emojis': emojis,'Shortcodes': [f':{code}:' for code in codes]})

st.title("These are streamlit emojis")
st.table(df)
