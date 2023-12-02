import pandas as pd
import streamlit as st
import altair as alt
import overwatch
 
if __name__ == '__main__':
    ow_data = overwatch.ow_data

    ow_data = ow_data[(ow_data['hero'] == 'Ashe') | (ow_data['hero'] == 'Ana' )]

    ow_data

    st.markdown("---")
    label = pd.DataFrame({"Column 1": [1,2,3,4,5]})
    st.markdown("<h1 style='text-align: center; color: black;'>Benny is better than Syd at Overwatch</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: grey;'>See proof below :) </h4>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header('Filters')

    # Select box for filtering data based on a category
    #selected_hero = st.sidebar.selectbox('Select a Hero:', ow_data['hero'].unique())
    #st.header(f'Data for Hero: {selected_hero}')
    selected_metric = st.sidebar.selectbox('Select a Metric:', ow_data['metric'].unique())

    # Filter the data based on user selections
    filtered_df = ow_data[ow_data['metric'] == selected_metric]

    chart=alt.Chart(filtered_df).mark_bar(strokeWidth=100).encode(
    x=alt.X('url:N', title="", scale=alt.Scale(paddingOuter=0.5)),#paddingOuter - you can play with a space between 2 models 
    y='value:Q',
    color='hero:N',
    column=alt.Column('hero:N', title="", spacing =0), #spacing =0 removes space between columns, column for can and st 
    ).properties( width = 300, height = 300, ).configure_header(labelOrient='bottom').configure_view(
        strokeOpacity=0)

    st.altair_chart(chart, theme="streamlit") 