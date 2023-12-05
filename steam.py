import pandas as pd
import streamlit as st
import altair as alt

df = pd.read_csv('steam.csv', 
                 sep=',',           # Specify the column separator (default is ',')
                 header=0,          # Use the first row as column names
                 index_col=None,    # Do not use any column as the index
                 encoding='utf-8',  # Specify the file encoding
                 nrows=None         # Read only the first n rows
                 )

print(df)