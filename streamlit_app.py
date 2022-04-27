import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')


#overall happiness
overall_happiness = alt.Chart(df).mark_circle().encode(
    alt.X('1_happy_now:Q'),
    alt.Y('count():Q'))
st.altair_chart(overall_happiness, use_container_width=False)
