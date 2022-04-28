import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')

st.set_page_config(
    page_title="Somerville Happiness Survey 2021", page_icon="📊", initial_sidebar_state="expanded"
)
st.title('Somerville Happiness Survey 2021')




#CHARTS

#overall happiness
overall_happiness = alt.Chart(df_happy).mark_bar(size = 30).encode(
    alt.X('1_happy_now:O', title = 'On a scale of 0 to 10, how happy are you right now?'), 
    alt.Y('count():Q', title = 'Number of responses'))






navigation = st.sidebar.radio("Explore the data by:", ('Overall trends', 'Gender','Age', 'Income')) 

if navigation == 'Overall trends':
    st.altair_chart(overall_happiness, use_container_width=True)
if navigation == 'Gender': 
    pass
if navigation == 'Age':
    pass
if navigation == 'Income':
    pass
else:
    pass
    
