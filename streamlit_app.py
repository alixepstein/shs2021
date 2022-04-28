import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')

st.set_page_config(
    page_title="Somerville Happiness Survey 2021", page_icon="📊", initial_sidebar_state="expanded")
st.title('Somerville Happiness Survey 2021')





#CHARTS

#overall happiness
overall_happiness = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('1_happy_now:Q', title = 'On a scale of 0 to 10, how happy are you right now?'), 
    alt.Y('count():Q', title = 'Number of responses')).properties(title = 'Overall Happiness')


#overall satisfaction with Somerville
overall_satis = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('3_satisfied_somerville:Q', title = 'How satisfied are you with Somerville as a place to live?'),
    alt.Y('count():Q', title = 'Number of responses')).properties(
    title='Overall Satisfaction with Somerville')






#NAVIGATION SIDEBAR

navigation = st.sidebar.radio("Explore the data by:", ('Introduction', 'Overall trends', 'Gender','Age', 'Income')) 

if navigation == 'Introduction':
    st.markdown('Some description about the survey')
    st.image(['Somerville Happiness Survey 2021 English.jpg', 'page2 Somerville Happiness Survey 2021 English.jpg'], width = 400, caption = ['1', '2'])
    
    
if navigation == 'Overall trends':
    st.subheader('Overall trends')
    st.altair_chart(overall_happiness)
    st.altair_chart(overall_satis)
if navigation == 'Gender': 
    st.subheader('Gender')
if navigation == 'Age':
    st.subheader('Age')
if navigation == 'Income':
    st.subheader('Income')
else:
    pass
    
