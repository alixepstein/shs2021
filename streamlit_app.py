import pandas as pd
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')


#overall happiness
overall_happiness = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('1_happy_now:O'),
    alt.Y('count():Q'))
st.altair_chart(overall_happiness, use_container_width=False)
