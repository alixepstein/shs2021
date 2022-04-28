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

#overall response to question is Somerville heading in the right direction or on the wrong track?
df_right_direction = df.dropna(subset=['5_right_direction'])
right_direction = alt.Chart(df_right_direction).mark_bar(size = 35).encode(
    alt.X('5_right_direction', title = None),
    alt.Y('count()', title = 'Number of responses')).properties(width = 200)

#satisfaction by age - binned (smooth) average line and unbinned (jagged) average line
yabin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', bin = True, title = 'Age in years'),
    alt.Y('mean(avg_satis_age):Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age')
nabin = bin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', title = 'Age in years'),
    alt.Y('avg_satis_age:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age')
satis_over_age = yabin + nabin

#satisfaction by income
income_categories = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to 74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to 200,000', '$200,000 or more']
satis_income = alt.Chart(df.dropna()).mark_bar().encode(
    alt.X('d9_income:N', sort = income_categories, title = 'Household income'),
    alt.Y('avg_satis_income:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by income')






#NAVIGATION SIDEBAR

navigation = st.sidebar.radio("Explore the data by:", ('Introduction', 'Overall trends', 'Gender','Age', 'Income')) 

if navigation == 'Introduction':
    
    st.markdown('Some description about the survey')
    
    st.markdown('Some introduction to this is what the survey looked like')
    col1, col2 = st.columns(2)
    with col1:
        st.image('Somerville Happiness Survey 2021 English.jpg', caption = '1')
    with col2:
        st.image('page2 Somerville Happiness Survey 2021 English.jpg', caption = '2')

    
    
    
if navigation == 'Overall trends':
    
    st.subheader('Overall trends')
    st.markdown('Some description')
    
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(overall_happiness)
    with col2:
        st.altair_chart(overall_satis)
    st.text('')
    st.markdown('Overall response to question is Somerville heading in the right direction or on the wrong track?')
    st.altair_chart(right_direction)
    
    
    
if navigation == 'Gender': 
    st.subheader('Gender')
    
    
if navigation == 'Age':
    st.subheader('Age')
    st.markdown('Some description')
    st.altair_chart(satis_over_age)
    
if navigation == 'Income':
    st.subheader('Income')
    st.markdown('Some description')
    st.altair_chart(satis_income)
    
else:
    pass
    
