import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')

st.set_page_config(
    page_title="Somerville Happiness Survey 2021", page_icon="📊", initial_sidebar_state="expanded")
st.title('Somerville Happiness Survey 2021')





#CHARTS

#OVERALL

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

#AGE

#satisfaction by age - binned (smooth) average line and unbinned (jagged) average line
yabin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', bin = True, title = 'Age in years'),
    alt.Y('mean(avg_satis_age):Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age')
nabin = bin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', title = 'Age in years'),
    alt.Y('avg_satis_age:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age')
satis_over_age = yabin + nabin

#INCOME

#satisfaction by income
income_categories = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to 74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to 200,000', '$200,000 or more']
satis_income = alt.Chart(df.dropna()).mark_bar().encode(
    alt.X('d9_income:O', sort = income_categories, title = 'Household income'),
    alt.Y('avg_satis_income:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by income', height = 400)

#dropdown list - income - satisfaction
income_satis_input_dropdown = alt.binding_select(options = income_categories)
income_satis_selection = alt.selection_single(fields=['d9_income'], bind=income_satis_input_dropdown, name='Income')
income_dropdown_satis = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('3_satisfied_somerville:Q', sort = income_categories, title = 'Satisfaction with living in Somerville'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#RACE

#satisfaction by race
satis_race_chart = [
    ['White', 7.367925],
    ['Asian', 7.867647],
    ['Mixed Race', 7.600000],
    ['Hispanic/Latino', 7.857143],
    ['Black', 7.259259]]
df_satis_race = pd.DataFrame(satis_race_chart, columns=['Race', 'Satisfaction'])
satis_race = alt.Chart(df_satis_race).mark_bar().encode(
    alt.X('Race:N'),
    alt.Y('Satisfaction:Q', title = None)).properties(title = 'Satisfaction living in Somerville by race')

#GENDER

#satisfaction by gender
df_gender = df[df['d1_gender'] != 'No Gender Given']
satis_gender = alt.Chart(df_gender).mark_bar().encode(
    alt.X('d1_gender:N', title = 'Gender', sort = ['Male', 'Female', 'Gender Non_Conforming']),
    alt.Y('avg_satis_gender:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by gender', height = 400)


#WARD

df_ward = df[df['Ward'] != 'No Answer Given']
ward_list = list(df_ward['Ward'].unique())
ward_list.sort()

#rating of housing cost by ward
ward_housing_cost = alt.Chart(df_ward).mark_bar().encode(
    alt.X('Ward:N'),
    alt.Y('avg_housing_cost_ward:Q', title = 'rating of housing cost')).properties(title = 'Rating of housing cost by ward')

#rating of maintenance of streets and sidewalks by ward
ward_streets_sidewalks = alt.Chart(df_ward).mark_bar().encode(
    alt.X('Ward:N'),
    alt.Y('avg_streets_sidewalks_ward:Q', title = 'rating of maintenance of streets/sidewalks')).properties(
    title = 'Rating of maintenance of streets/sidewalks by ward')

#rating of feeling of safety when walking at night by ward
ward_safe_night = alt.Chart(df_ward).mark_bar().encode(
    alt.X('Ward:N'),
    alt.Y('avg_safe_night_ward:Q', title = 'How safe do you feel at night?')).properties(
    title = 'How safe people feel at night by ward')

#rating of beauty of neighborhood by ward
ward_beauty = alt.Chart(df_ward).mark_bar().encode(
    alt.X('Ward:N'),
    alt.Y('avg_neighborhood_beauty_ward:Q', title = 'Rating of neighborhood beauty')).properties(
    title = 'Rating of neighborhood beauty by ward')

#dropdown list - wards - satisfaction
ward_satis_input_dropdown = alt.binding_select(options = ward_list)
ward_satis_selection = alt.selection_single(fields=['Ward'], bind=ward_satis_input_dropdown, name='Somerville')
ward_dropdown_satis = alt.Chart(df_ward).mark_bar().encode(
    alt.X('3_satisfied_somerville:O', title = 'Satisfaction with living in Somerville'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')).add_selection(
    ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - satisfaction with your neighborhood
ward_dropdown_neighborhood_satis = alt.Chart(df).mark_bar().encode(
    alt.X('4_satisfied_neighborhood:O', title = 'Satisfaction with your neighborhood'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - is somerville heading in the right direction
ward_dropdown_right_direction = alt.Chart(df).mark_bar().encode(
    alt.X('5_right_direction:N', title = 'Is Somerville heading in the right direction?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - rating of maintenance of streets and sidewalks
ward_dropdown_streets_sidewalks = alt.Chart(df).mark_bar().encode(
    alt.X('6e_streets_sidewalks:O', title = 'Rating of maintenance of streets/sidewalks'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - feeling of safety crossing the street
ward_dropdown_street_crossing = alt.Chart(df).mark_bar().encode(
    alt.X('9_street_crossing:O', title = 'How safe do you feel crossing the street?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - convenience going places
ward_dropdown_convenient_go = alt.Chart(df).mark_bar().encode(
    alt.X('10_convenient_go:O', title = 'How convenient is it go places?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - feeling of safety at night
ward_dropdown_safe_at_night = alt.Chart(df).mark_bar().encode(
    alt.X('11_safe_at_night:Q', title = 'How safe do you feel at night?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - age
ward_dropdown_age = alt.Chart(df).mark_bar().encode(
    alt.X('d2_age:Q', title = 'Age', bin = True),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - race
ward_dropdown_race = alt.Chart(df).mark_bar().encode(
    alt.X('d4_race:N', title = 'Race'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection).properties(
    height = 300)

#dropdown - ward - rent/own
ward_dropdown_rent_own = alt.Chart(df).mark_bar().encode(
    alt.X('d7_rent_own:N', title = 'Housing status'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - plans to move
ward_dropdown_moving = alt.Chart(df).mark_bar().encode(
    alt.X('d8a_moving:N', title = 'Plans to move'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - income
ward_dropdown_income = alt.Chart(df).mark_bar().encode(
    alt.X('d9_income:N', title = 'Income'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)





#RENTING OWNING HOUSING COST CONCERNS

#satisfaction by rent/own status
avg_rent_own_satis = [
    ['Rent', 7.312757],
    ['Own', 7.510204]]
df_rent_own_satis = pd.DataFrame(avg_rent_own_satis, columns=['Housing Status', 'Satisfaction'])
rent_own_satis = alt.Chart(df_rent_own_satis).mark_bar().encode(
    alt.X('Satisfaction:Q', title = None),
    alt.Y('Housing Status:N')).properties(height=50)

#satisfaction by plans to move
avg_moving_satis = [
    ['Planning to Move', 6.447447],
    ['No Plan to Move', 8.031304]]
df_moving_satis = pd.DataFrame(avg_moving_satis,columns=['Planning to Move','Satisfaction'])
moving_satis = alt.Chart(df_moving_satis).mark_bar().encode(
    alt.X('Satisfaction:Q', title = 'Satisfaction', scale = alt.Scale(domain = (0,8))),
    alt.Y('Planning to Move:N'))





#NAVIGATION SIDEBAR

navigation = st.sidebar.radio("Explore the data by:", ('Introduction', 'Overall trends', 'Age', 'Gender', 'Income', 'Race', 'Ward', 'Housing cost')) 

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
    st.markdown('Some description')
    st.altair_chart(satis_gender)
    
if navigation == 'Age':
    st.subheader('Age')
    st.markdown('Some description')
    st.altair_chart(satis_over_age)
    
if navigation == 'Income':
    st.subheader('Income')
    st.markdown('Some description')
    st.altair_chart(satis_income)
    st.header('')
    st.altair_chart(income_dropdown_satis)
    
if navigation == 'Race':
    st.subheader('Race')
    st.markdown('Some description')
    st.altair_chart(satis_race)
    
if navigation == 'Ward':
    st.subheader('Ward')
    st.markdown('Somerville is divided into seven wards of roughly equal size. Here you can explore how survey results differed by which ward respondent lived in.')
    st.header('')
    st.image('ward map.png')
    st.caption('This map shows average happiness ratings by ward. There was not an appreciable difference in happiness between wards. Ward 5 reported the highest average happiness at 7.6, while its neighbor, Ward 3, reported the lowest average happiness at 7.03. The range in happiness between wards was about half a point')   
    st.header('')
    st.altair_chart(ward_dropdown_satis)
    st.altair_chart(ward_dropdown_neighborhood_satis)
    st.altair_chart(ward_dropdown_right_direction)
    st.altair_chart(ward_dropdown_streets_sidewalks)
    st.altair_chart(ward_dropdown_street_crossing)
    st.altair_chart(ward_dropdown_convenient_go)
    st.altair_chart(ward_dropdown_safe_at_night)
    st.altair_chart(ward_dropdown_age)
    st.altair_chart(ward_dropdown_race)
    st.altair_chart(ward_dropdown_rent_own)
    st.altair_chart(ward_dropdown_moving)
    st.altair_chart(ward_dropdown_income)
    
    st.header('')
    st.markdown('Here are some average responses by ward:')
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(ward_housing_cost)
        st.altair_chart(ward_safe_night)
    with col2:
        st.altair_chart(ward_streets_sidewalks)
        st.altair_chart(ward_beauty)
    
    
if navigation == 'Housing cost':
    st.subheader('Housing cost, renting, owning, and other concerns')
    st.markdown('Some description')
    st.text('')
    
    
    
else:
    pass


    
