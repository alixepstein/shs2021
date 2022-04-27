import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')

st.set_page_config(
    page_title="Somerville Happiness Survey 2021", page_icon="📊", initial_sidebar_state="expanded"
)
st.title('Somerville Happiness Survey 2021')


#overall happiness
overall_happiness = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('1_happy_now:Q'),
    alt.Y('count():Q'))
st.altair_chart(overall_happiness, use_container_width=False)
