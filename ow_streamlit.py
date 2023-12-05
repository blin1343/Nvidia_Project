import pandas as pd
import streamlit as st
import altair as alt
import overwatch
 
if __name__ == '__main__':

    ow_data = overwatch.ow_data

    # Row A: Set up page config, titles, and notes & assumptions
    st.set_page_config(
        page_title="Overwatch Stat Tracker",
        page_icon="https://seeklogo.com/images/O/overwatch-logo-932A9F60A4-seeklogo.com.png",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            'About': "https://github.com/blin1343/Nvidia_Project"
            }
    )

    tab1, tab2 = st.tabs(["Dashboard", "Data"])

    with tab1:
        #col1, col2, = st.columns([1,1])
        st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Overwatch_2_text_logo.svg/2560px-Overwatch_2_text_logo.svg.png',width=700)
        st.markdown("<h1 style='text-align: center; color: black;'>Stat Tracker</h1>", unsafe_allow_html=True)
        st.markdown("---")

        st.text_area(
            "***Notes & Assumptions***",
            "* Data is scraped from Blizzard's offical OW2 career profile page\n"
            "* Data only includes blin1343 & takaharimi profiles\n"
            "* Data will not include player's with profiles set to private\n"
            "\n"
            "Metric Defintions:\n"
            "* All Damage Done - Avg. damage done to other players (including shields & objects) per 10 minutes\n"
            "* Final Blows - Avg. number of eliminations where the player landed the final blow per 10 minutes\n"
            "* Deaths - Avg. number of deaths per 10 minutes\n"
            "* Hero Damage Done - Avg. damage done to other players (excluding shields & objects) per 10 minutes\n"
            "* Eliminations - Avg. number of eliminations that involved the player per 10 minutes\n"
            "* Healing Done - Avg. amount healed per 10 minutes (support role can only heal)",
            height = 200
        )

        st.write(f"\n")

        # Row B: Sidebar & Filters
        st.sidebar.header('Filters')

        all_heroes = sorted(ow_data['hero'].unique())
        all_roles = sorted(ow_data['role'].unique())
        all_metrics = sorted(ow_data['metric'].unique())

        role_filter = st.sidebar.selectbox('Select Role', all_roles)
        hero_filter = st.sidebar.multiselect('Select Hero (Multi-Select)', sorted(ow_data[ow_data['role'] == role_filter]['hero'].unique()))
        metric_filter = st.sidebar.selectbox('Select Metric', sorted(ow_data[ow_data['role'] == role_filter]['metric'].unique()))

       # Row C: Top Level Metrics
        elims = ow_data[(ow_data['metric'] == 'Eliminations - Avg per 10 Min') & (ow_data['role'] == role_filter)].groupby(['role'])['value'].mean()
        healing = ow_data[(ow_data['metric'] == 'Healing Done - Avg per 10 Min') & (ow_data['role'] == role_filter)].groupby(['role'])['value'].mean()
        deaths = ow_data[(ow_data['metric'] == 'Deaths - Avg per 10 Min') & (ow_data['role'] == role_filter)].groupby(['role'])['value'].mean()

        # Check if the multiselect is empty
        if not hero_filter:
            st.warning("Please select a hero(s) to get started.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric(f"{role_filter} Eliminations - Avg per 10 Min", round(elims, 2))
            col2.metric(f"{role_filter} Healing Done - Avg per 10 Min", round(healing, 2))
            col3.metric(f"{role_filter} Deaths - Avg per 10 Min", round(deaths, 2))
            
            st.markdown("---")

            filtered_df = ow_data[(ow_data['role'] == role_filter) & (ow_data['hero'].isin(hero_filter)) & (ow_data['metric'] == metric_filter)]

            st.write(f"Comparing the {metric_filter} metric")
            chart = alt.Chart(filtered_df).mark_bar().encode(
                x=alt.X('value:Q',title=""),
                y=alt.Y('url', title=""),
                color='url:N',
                row='hero:N',
                tooltip=['hero', 'role', 'url', 'value']
            ).properties( autosize=alt.AutoSizeParams
                ( type="fit",
                resize=True ,
                contains="padding"
                )
            )
                
            st.altair_chart(chart, theme="streamlit") 

    with tab2:
         st.dataframe(ow_data, use_container_width=True)