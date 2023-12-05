import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

df = pd.read_csv('data/steam.csv', sep=',', header=0, index_col=None, encoding='utf-8', nrows=None)

st.set_page_config(
        page_title="Steam",
        page_icon="https://static.vecteezy.com/system/resources/previews/020/975/557/original/steam-logo-steam-icon-transparent-free-png.png",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            'About': "https://github.com/blin1343/Nvidia_Project"
            }
    )

years = sorted(df['release_date'].unique().tolist())
year =  st.sidebar.selectbox('Which year', years, 0)
df[df['release_date'] == year]

st.markdown("<h1 style='text-align: center; color: black;'>Prices of games on Steam over time</h1>", unsafe_allow_html=True)
st.markdown("---")

st.text_area(
    "***Notes & Assumptions***",
    "* Work in Progress\n",
    height = 200
)

df=df.groupby(['release_date'])['price'].mean().reset_index()

fig = px.line(df, x="release_date", y="price")
fig.update_layout(width=800)
