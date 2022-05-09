import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

df = pd.read_csv('SHSdf.csv')

st.set_page_config(
    page_title="Somerville Happiness Survey 2021", page_icon="📊", initial_sidebar_state="expanded")
st.image('shs banner.png')
cola, colb, colc = st.columns([4.6,1,5.5])
with colb:
    st.subheader('2021')


#CHARTS

#OVERALL

#overall happiness
overall_happiness = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('1_happy_now:Q', title = 'On a scale of 0 to 10, how happy are you right now?'), 
    alt.Y('count():Q', title = 'Number of responses')).properties(title = 'Overall Happiness')

#overall satisfaction with Somerville
overall_satis = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('3_satisfied_somerville:Q', title = 'How satisfied are you with Somerville as a place to live?'),
    alt.Y('count():Q', title = 'Number of responses')).properties(
    title='Overall Satisfaction with Somerville')

#overall response to question is Somerville heading in the right direction or on the wrong track?
df_right_direction = df.dropna(subset=['5_right_direction'])
right_direction = alt.Chart(df_right_direction).mark_bar(size = 35).encode(
    alt.X('5_right_direction', title = None),
    alt.Y('count()', title = 'Number of responses')).properties(width = 200)

#overall averages
total_average_order = ['Rate the availability of information about city services',  
    'How safe do you feel walking in your neighborhood at night?', 'Rate the appearance of parks and squares in your neighborhood', 
    'How satisfied are you with your life in general?', 'How satisfied are you with your neighborhood?', 
    'Rate the condition of your housing', 'How satisfied are you with Somerville as a place to live?',
    'Rate the availability of social community events', 'How happy do you feel right now?', 'Rate your ability to access City services in the past year',
    'How convenient is it for you to get where you want to go?', 'Rate the beauty or physical setting of your neighborhood',
    'Rate the overall quality of public schools', 'Rate your trust in the local police', 'How safe do you feel crossing a busy street in Somerville?',
    'Rate the maintenance of streets and sidewalks', 'Rate the cost of housing']
total_averages = [
    ['How happy do you feel right now?', 7.305296/10],['How satisfied are you with your life in general?', 7.619543/10],['How satisfied are you with Somerville as a place to live?', 7.372141/10],['How satisfied are you with your neighborhood?', 7.569072/10],['Rate the availability of information about city services', 3.940252/5],['Rate the cost of housing', 2.115589/5],['Rate the overall quality of public schools', 3.407947/5],['Rate your trust in the local police', 3.379421/5],['Rate the maintenance of streets and sidewalks', 2.986472/5],['Rate the availability of social community events', 3.651982/5],['How safe do you feel crossing a busy street in Somerville?', 6.698035/10],['How convenient is it for you to get where you want to go?', 7.188017/10],['How safe do you feel walking in your neighborhood at night?', 7.746082/10],['Rate the appearance of parks and squares in your neighborhood', 7.637500/10],['Rate the beauty or physical setting of your neighborhood', 7.064651/10],['Rate the condition of your housing', 7.492723/10],['Rate your ability to access City services in the past year', 7.197611/10]]
df_total_averages = pd.DataFrame(total_averages,columns=['Question','Rating'])
total_averages_chart = alt.Chart(df_total_averages).mark_bar().encode(
    alt.X('Rating:Q', scale=alt.Scale(domain=(0, 1))),
    alt.Y('Question:N', title = None, sort = total_average_order, axis=alt.Axis(labelLimit=400))).properties(title = 'Average ratings')
#AGE

#satisfaction by age - binned (smooth) average line and unbinned (jagged) average line
yabin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', bin = True, title = 'Age in years'),
    alt.Y('mean(avg_satis_age):Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age', width = 350)
nabin = bin = alt.Chart(df).mark_line().encode(
    alt.X('d2_age:Q', title = 'Age in years'),
    alt.Y('avg_satis_age:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by age', width = 350)
satis_over_age = yabin + nabin

#ages with responsive bins
brush = alt.selection_interval(encodings=['x'])
responses_age = alt.Chart(df).mark_bar().encode(
    alt.X('d2_age:Q', title = 'Age', bin = True),
    alt.Y('count():Q', title = 'Number of Responses')).properties(width = 350)
age_bin_brush = alt.hconcat(
    responses_age.encode(alt.X('d2_age:Q',title = 'Age', bin=alt.Bin(
        maxbins=30, extent=brush), axis=alt.Axis(
        format='d'),scale=alt.Scale(domain=brush))), responses_age.encode(
        alt.X('d2_age:Q', title = 'Age', bin=alt.Bin(maxbins=9)),).add_selection(brush))

#INCOME

#satisfaction by income
income_categories = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to 74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to 200,000', '$200,000 or more']
satis_income = alt.Chart(df.dropna()).mark_bar().encode(
    alt.X('d9_income:O', sort = income_categories, title = 'Household income'),
    alt.Y('avg_satis_income:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by income', height = 400)

#dropdown list - income - satisfaction
income_satis_input_dropdown = alt.binding_select(options = income_categories)
income_satis_selection = alt.selection_single(fields=['d9_income'], bind=income_satis_input_dropdown, name='Income')
income_dropdown_satis = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('3_satisfied_somerville:Q', sort = income_categories, title = 'Satisfaction with living in Somerville'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - satisfaction with your neighborhood
income_dropdown_neighborhood_satis = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('4_satisfied_neighborhood:Q', title = 'Satisfaction with your neighborhood'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - is somerville heading in the right direction
income_dropdown_right_direction = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('5_right_direction:N', title = 'Is Somerville heading in the right direction?'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - rating of maintenance of streets and sidewalks
income_dropdown_streets_sidewalks = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('6e_streets_sidewalks:Q', title = 'Rating of maintenance of streets/sidewalks'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - feeling of safety crossing the street
income_dropdown_street_crossing = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('9_street_crossing:Q', title = 'How safe do you feel crossing the street?'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - convenience going places
income_dropdown_convenient_go = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('10_convenient_go:Q', title = 'How convenient is it go places?'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - feeling of safety at night
income_dropdown_safe_at_night = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('11_safe_at_night:Q', title = 'How safe do you feel at night?'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - age
income_dropdown_age = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('d2_age:Q', title = 'Age', bin = True),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - race
income_dropdown_race = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('d4_race:N', title = 'Race'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - rent/own
income_dropdown_rent_own = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('d7_rent_own:N', title = 'Housing status'),
    alt.Y('count():Q', title = 'Number of responses per selected income')).add_selection(
    income_satis_selection).transform_filter(income_satis_selection)

#dropdown - income - plans to move
income_dropdown_moving = alt.Chart(df).mark_bar(size = 20).encode(
    alt.X('d8a_moving:N', title = 'Plans to move'),
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
    alt.Y('Race:N'),
    alt.X('Satisfaction:Q', title = None)).properties(title = 'Satisfaction living in Somerville by race')

#GENDER

#satisfaction by gender
df_gender = df[df['d1_gender'] != 'No Gender Given']
satis_gender = alt.Chart(df_gender).mark_bar().encode(
    alt.Y('d1_gender:N', title = 'Gender', sort = ['Male', 'Female', 'Gender Non_Conforming']),
    alt.X('avg_satis_gender:Q', title = 'Satisfaction living in Somerville')).properties(title = 'Satisfaction living in Somerville by gender')

#WARD

df_ward = df[df['Ward'] != 'No Answer Given']
ward_list = list(df_ward['Ward'].unique())
ward_list.sort()
df_ward['3_satisfied_somerville'].dropna(inplace = True)
df_ward[['4_satisfied_neighborhood', '5_right_direction', '6e_streets_sidewalks', '9_street_crossing', '10_convenient_go', '11_safe_at_night', 'd2_age', 'd4_race', 'd7_rent_own', 'd8a_moving', 'd9_income']].dropna(inplace = True)

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
ward_dropdown_neighborhood_satis = alt.Chart(df_ward).mark_bar().encode(
    alt.X('4_satisfied_neighborhood:O', title = 'Satisfaction with your neighborhood'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - is somerville heading in the right direction
ward_dropdown_right_direction = alt.Chart(df_ward).mark_bar().encode(
    alt.X('5_right_direction:N', title = 'Is Somerville heading in the right direction?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - rating of maintenance of streets and sidewalks
ward_dropdown_streets_sidewalks = alt.Chart(df_ward).mark_bar().encode(
    alt.X('6e_streets_sidewalks:O', title = 'Rating of maintenance of streets/sidewalks'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - feeling of safety crossing the street
ward_dropdown_street_crossing = alt.Chart(df_ward).mark_bar().encode(
    alt.X('9_street_crossing:O', title = 'How safe do you feel crossing the street?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - convenience going places
ward_dropdown_convenient_go = alt.Chart(df_ward).mark_bar().encode(
    alt.X('10_convenient_go:O', title = 'How convenient is it go places?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - feeling of safety at night
ward_dropdown_safe_at_night = alt.Chart(df_ward).mark_bar().encode(
    alt.X('11_safe_at_night:O', title = 'How safe do you feel at night?'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - age
ward_dropdown_age = alt.Chart(df_ward).mark_bar().encode(
    alt.X('d2_age:Q', title = 'Age', bin = True),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - race
ward_dropdown_race = alt.Chart(df_ward).mark_bar().encode(
    alt.X('d4_race:N', title = 'Race'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection).properties(
    height = 300)

#dropdown - ward - rent/own
ward_dropdown_rent_own = alt.Chart(df_ward).mark_bar().encode(
    alt.X('d7_rent_own:N', title = 'Housing status'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - plans to move
ward_dropdown_moving = alt.Chart(df_ward).mark_bar().encode(
    alt.X('d8a_moving:N', title = 'Plans to move'),
    alt.Y('count():Q', title = 'Number of responses per selected ward')
    ).add_selection(ward_satis_selection).transform_filter(ward_satis_selection)

#dropdown - ward - income
ward_dropdown_income = alt.Chart(df_ward).mark_bar().encode(
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
    alt.Y('Housing Status:N'))

#satisfaction by plans to move
avg_moving_satis = [
    ['Planning to Move', 6.447447],
    ['No Plan to Move', 8.031304]]
df_moving_satis = pd.DataFrame(avg_moving_satis,columns=['Planning to Move','Satisfaction'])
moving_satis = alt.Chart(df_moving_satis).mark_bar().encode(
    alt.X('Satisfaction:Q', title = 'Satisfaction', scale = alt.Scale(domain = (0,8))),
    alt.Y('Planning to Move:N'))

df_rent_own = df[df['d7_rent_own'] != 'No Answer Given']
moving_housing_status_horiz = alt.Chart(df_rent_own).mark_bar().encode(
    alt.Y('d7_rent_own:N', title = 'Housing Status'),
    alt.X('count():Q', title = 'Number of Responses'),
    color = alt.Color('d8a_moving:N', legend = alt.Legend(title = 'Plan to leave Somerville')))
moving_housing_status_vert = alt.Chart(df_rent_own).mark_bar().encode(
    alt.X('d7_rent_own:N', title = 'Housing Status'),
    alt.Y('count():Q', title = 'Number of Responses'),
    color = alt.Color('d8a_moving:N', legend = alt.Legend(title = 'Plan to leave Somerville')))


# rent or own by income
income_rent_own = [['$200,000 or more', 'Own', 0.7388888888888889],
    ['$200,000 or more', 'Rent', 0.2611111111111111],['$150,000 to $199,999', 'Own', 0.4460431654676259],['$150,000 to $199,999', 'Rent', 0.5539568345323741],['$100,000 to $149,999', 'Own', 0.5],['$100,000 to $149,999', 'Rent', 0.5],['$75,000 to $99,999', 'Own', 0.43846153846153846],['$75,000 to $99,999', 'Rent', 0.5615384615384615],['$50,000 to $74,999', 'Own', 29/(29+80)],['$50,000 to $74,999', 'Rent', 80/(29+80)],['$25,000 to $49,999', 'Own', 28/(28+48)],['$25,000 to $49,999', 'Rent', 0.631578947368421],['$10,000 to $24,999', 'Own', 0.2807017543859649],['$10,000 to $24,999', 'Rent', 0.7192982456140351],['Less than $10,000', 'Own', 0.1935483870967742],['Less than $10,000', 'Rent', 0.8064516129032258]]
df_income_rent = pd.DataFrame(income_rent_own,columns=['Income', 'Housing Status', 'Total'])
income_order = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to $74,999',
    '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 to $199,999', '$200,000 or more']
rent_income = alt.Chart(df_income_rent).mark_bar().encode(
    alt.X('Income:N', sort = income_order),
    alt.Y('Total:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Housing Status:N', sort = ['Own', 'Rent'], legend = alt.Legend(title = 'Rent or own')))

#rent or own by race
#percentage by race = 
df_rent = df[df['d7_rent_own'] != 'No Answer Given']
rro = df_rent.groupby('d4_race')['d7_rent_own'].value_counts(normalize = True)
race_rent_own = [['Asian', 'Rent', rro[0]],
    ['Asian', 'Own', rro[1]],
    ['Black/African American', 'Rent', rro[2]],
    ['Black/African American', 'Own', rro[3]],
    ['Hispanic/Latino', 'Rent', rro[4]],
    ['Hispanic/Latino', 'Own', rro[5]],
    ['White', 'Rent', rro[11]],
    ['White', 'Own', rro[12]]]
df_race_rent = pd.DataFrame(race_rent_own,columns=['Race', 'Housing Status', 'Percentage'])
rent_race = alt.Chart(df_race_rent).mark_bar().encode(
    alt.X('Race:N', sort = ['White', 'Asian', 'Black/African American', 'Hispanic/Latino']),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Housing Status:N', sort = ['Own', 'Rent'], legend = alt.Legend(title = 'Rent or own')))

#plans to move by race
race_moving = [['Asian', 'No', 0.656716],
    ['Asian', 'Yes', 0.343284],['Black/African American', 'No', 0.612903],['Black/African American', 'Yes', 0.387097],['Hispanic/Latino', 'No', 0.580000],['Hispanic/Latino', 'Yes', 0.420000],['White', 'No', 0.648951],['White', 'Yes', 0.351049]]
df_race_moving = pd.DataFrame(race_moving,columns=['Race', 'Plan to Move Yes/No', 'Percentage'])
move_race = alt.Chart(df_race_moving).mark_bar().encode(
    alt.X('Race:N', sort = ['Asian', 'White', 'Black/African American', 'Hispanic/Latino']),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Plan to Move Yes/No:N', legend = alt.Legend(title = 'Plans to move')))

#plans to move by whether or not you live with children under 18
children_moving = [
    ['No children', 'No', 0.620081],['No children', 'Yes', 0.379919],['Yes children', 'No', 0.704918],['Yes children', 'Yes', 0.295082]]
df_children_moving = pd.DataFrame(children_moving,columns=['Children yes/no', 'Plan to Move Yes/No', 'Percentage'])
move_children = alt.Chart(df_children_moving).mark_bar().encode(
    alt.X('Children yes/no:N'),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Plan to Move Yes/No:N', legend = alt.Legend(title = 'Plans to move')))

#rent or own by age
df_num = df[df['d2_age'] != 'No Age Given']
df_num['d2_age'] = pd.to_numeric(df_num['d2_age'])
age_bins = df_num.groupby(['d7_rent_own', pd.cut(df_num['d2_age'], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])])
age_bins.size().unstack()
age_rent_own = [
    ['10', 'Own', .5],['10', 'Rent', .5],['20', 'Own', 20/(189)],['20', 'Rent', 169/189],['30', 'Own', 92/(92+167)],['30', 'Rent', 167/(92+167)],['40', 'Own', 96/(96+49)],['40', 'Rent', 49/(96+49)],['50', 'Own', 88/(88+34)],['50', 'Rent', 34/(88+34)],['60', 'Own', 83/(83+40)],['60', 'Rent', 40/(83+40)],['70', 'Own', 45/(45+18)],['70', 'Rent', 18/(45+18)],['80', 'Own', 10/15],['80', 'Rent', 5/15]]
df_age_rent = pd.DataFrame(age_rent_own,columns=['Age', 'Housing Status', 'Percentage'])
rent_age = alt.Chart(df_age_rent).mark_bar().encode(
    alt.X('Age:N'),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Housing Status:N', legend = alt.Legend(title = 'Rent or own')))

#plans to move by age
age_bins = df_num.groupby(['d8a_moving', pd.cut(df_num['d2_age'], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90])])
age_bins.size().unstack()
age_moving = [
    ['10', 'Yes', .5],['10', 'No', .5],['20', 'Yes', 100/188],['20', 'No', 88/(188)],['30', 'Yes', 122/(133+122)],['30', 'No', 133/(133+122)],['40', 'Yes', 38/(101+38)],['40', 'No', 101/(101+38)],['50', 'Yes', 28/(92+28)],['50', 'No', 92/(92+28)],['60', 'Yes', 25/(89+25)],['60', 'No', 89/(89+25)],['70', 'Yes', 8/(57+8)],['70', 'No', 57/(57+8)],['80', 'Yes', 2/15],['80', 'No', 13/15],]
df_age_moving = pd.DataFrame(age_moving,columns=['Age', 'Plans to Move', 'Percentage'])
move_age = alt.Chart(df_age_moving).mark_bar().encode(
    alt.X('Age:N'),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Plans to Move:N', legend = alt.Legend(title = 'Plans to Move')))

#plans to move by income
income_moving = [
    ['$200,000 or more', 'No', 0.744318],['$200,000 or more', 'Yes', 0.255682],['$150,000 to $199,999', 'No', 0.514493],['$150,000 to $199,999', 'Yes', 0.485507],['$100,000 to $149,999', 'No', 0.573333],['$100,000 to $149,999', 'Yes', 0.426667],['$75,000 to $99,999', 'No', 0.612903],['$75,000 to $99,999', 'Yes', 0.387097],['$50,000 to $74,999', 'No', 0.571429],['$50,000 to $74,999', 'Yes', 0.428571],['$25,000 to $49,999', 'No', 0.697368],['$25,000 to $49,999', 'Yes', 0.302632],['$10,000 to $24,999', 'No', 0.727273],['$10,000 to $24,999', 'Yes', 0.272727],['Less than $10,000', 'No', 0.657143],['Less than $10,000', 'Yes', 0.342857]]
df_income_moving = pd.DataFrame(income_moving ,columns=['Income', 'Plans to Move', 'Percentage'])
move_income = alt.Chart(df_income_moving).mark_bar().encode(
    alt.X('Income:N', sort = income_order),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Plans to Move:N', legend = alt.Legend(title = 'Plans to Move')))

#rent or own by survey language
df.groupby('survey_language')['d7_rent_own'].value_counts()
language_rent_own = [
    ['English', 'Own', 438/(438+464)],['English', 'Rent', 464/(438+464)],['Portuguese', 'Own', 3/11],['Portuguese', 'Rent', 8/11],['Spanish', 'Own', 7/24],['Spanish', 'Rent', 17/24]]
df_language_rent = pd.DataFrame(language_rent_own,columns=['Language', 'Housing Status', 'Percentage'])
rent_language = alt.Chart(df_language_rent).mark_bar().encode(
    alt.X('Language:N', sort = ['English', 'Spanish', 'Portuguese']),
    alt.Y('Percentage:Q', title = 'Percentage', axis=alt.Axis(format='%')),
    color = alt.Color('Housing Status:N', legend = alt.Legend(title = 'Rent or own')))




#WHO ANSWERED THE SURVEY?

#ward
responses_ward = alt.Chart(df_ward).mark_bar().encode(
    alt.Y('Ward:O', title = 'Ward'),
    alt.X('count():Q', title = 'Number of Responses')).properties(width = 550)

#survey language
df_lang = df[df['survey_language'] != 'No Answer Given']
responses_language = alt.Chart(df_lang).mark_bar().encode(
    alt.Y('survey_language:N', title = 'Survey Language', sort = ['English', 'Spanish', 'Portuguese', 'Haitian Creole', 'Nepali']),
    alt.X('count():Q', title = 'Number of Responses')).properties(width = 550)

#gender
responses_gender = alt.Chart(df).mark_bar().encode(
    alt.Y('d1_gender:N', title = 'Gender', sort = ['Female', 'Male', 'No Gender Given', 'Gender Non_Conforming']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'What is your gender?', width = 550)

#age
responses_age = alt.Chart(df).mark_bar().encode(
    alt.Y('d2_age:Q', title = 'Age', bin = True),
    alt.X('count():Q', title = 'Number of Responses'))

#race
responses_race = alt.Chart(df).mark_bar().encode(
    alt.Y('d4_race:N', title = 'Race', axis=alt.Axis(labelLimit=400), sort = ['White', 'Asian', 'No Race Given', 'Hispanic or Latino', 'Black or African American Alone, Not Hispanic or Latino', 'Two or More Races, Not Hispanic or Latino', 'Some Other Race alone, Not Hispanic or Latino']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'What is your race?', width = 550)

#disability
responses_disability = alt.Chart(df).mark_bar().encode(
    alt.Y('d5_disability:N', title = 'Disability Status', sort = ['No', 'Yes', 'No Answer Given']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'Do you identify as having a disability and/or physical impairment?', width = 550)

#living with children under 18
responses_children = alt.Chart(df).mark_bar().encode(
    alt.Y('d6_children:N', title = 'Child(ren) under 18', sort = ['No', 'Yes', 'No Answer Given']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'Do you have children age 18 or younger who live with you?', width = 550)

#rent or own
responses_rent = alt.Chart(df).mark_bar().encode(
    alt.Y('d7_rent_own:N', title = 'Housing Status', sort = ['Rent', 'Own', 'No Answer Given']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'Describe your housing status in Somerville.', width = 550)

#plans to move
responses_moving = alt.Chart(df).mark_bar().encode(
    alt.Y('d8a_moving:N', title = 'Plans to move', sort = ['No', 'Yes', 'No Answer Given']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'Do you plan to move away from Somerville in the next two years?', width = 550)

#income
responses_income = alt.Chart(df).mark_bar().encode(
    alt.Y('d9_income:N', title = 'Income', sort = income_categories),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'What is your annual household income?', width = 550)

#students
responses_student = alt.Chart(df).mark_bar().encode(
    alt.Y('d10_student:N', title = 'Student?', sort = ['No', 'Yes', 'No Answer Given']),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'Are you a student?', width = 550)

#residence length
responses_res_length = alt.Chart(df).mark_bar().encode(
    alt.Y('d11_residence_length:Q', title = 'Length of residence in Somerville', bin = True),
    alt.X('count():Q', title = 'Number of Responses')).properties(title = 'How long have you lived in Somerville?', width = 550)

#census race data
census_race = ['Hispanic or Latino','White','Black or African American Alone, Not Hispanic or Latino','Asian','Some Other Race alone, Not Hispanic or Latino','Two or More Races, Not Hispanic or Latino']
census_race_totals = [7107, 48392, 3542, 7893, 1088, 3702]
census_order = ['White', 'Asian', 'Hispanic or Latino', 'Two or More Races, Not Hispanic or Latino', 'Black or African American Alone, Not Hispanic or Latino', 'Some Other Race alone, Not Hispanic or Latino']
census_source = pd.DataFrame({'a': census_race,'b': census_race_totals})

race_census = alt.Chart(census_source).mark_bar().encode(
    alt.Y('a', sort = census_order, axis=alt.Axis(labelLimit=400), title = 'Race'),
    alt.X('b', title = 'Population')).properties(title = '2020 Census Data', width = 550)






#NAVIGATION SIDEBAR

navigation = st.sidebar.radio("Explore the data by:", ('Introduction', 'Overall trends', 'Demographics', 'Income', 'Ward', 'Housing cost', 'Who answered the survey?')) 

if navigation == 'Introduction':
    
    st.markdown('The city of Somerville, Massachusetts, has been conducting its happiness survey every other year since 2011. The survey measures overall happiness, as well as satisfaction with specific aspects of living in Somerville. The results of the survey influence city policy and planning. On this page you will find the results of the 2021 Somerville Happiness Survey, arranged to make them easy to explore.')
    st.header('')
    st.markdown('The 2021 Somerville Happiness Survey was a two-page paper questionanaire, sent by standard mail to 5,000 households (randomly chosen and representative of the makeup of city population) in five languages (English, Spanish, Portuguese, Haitian Creole, and Nepali) in June of 2021. The survey included 15 happiness/satisfaction questions and 12 demographic questions.')
    col1, col2 = st.columns(2)
    with col1:
        st.image('Somerville Happiness Survey 2021 English.jpg', caption = '1')
    with col2:
        st.image('page2 Somerville Happiness Survey 2021 English.jpg', caption = '2')

    
    
    
if navigation == 'Overall trends':
    st.subheader('Overall trends')

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(overall_happiness, use_container_width=True)
    with col2:
        st.altair_chart(overall_satis, use_container_width=True)
    st.text('')
    st.markdown('Overall response to question "Is Somerville heading in the right direction or on the wrong track?"')
    cola, colb, colc = st.columns (3)
    with colb:
        st.altair_chart(right_direction)
    st.markdown('Average ratings of various aspects of life in Somerville (normalized to a scale of 0-1):')
    st.altair_chart(total_averages_chart, use_container_width=True)
    
    
    
if navigation == 'Demographics': 
    
    st.markdown('People tend to be about equally satisfied with living in Somerville, regardless of demographics.')
    
    
    st.subheader('Gender')
    st.altair_chart(satis_gender)
    
    st.subheader('Age')
    st.markdown('The smoother line is averaged by age group, while the jagged line is taken by individual year.')
    st.altair_chart(satis_over_age)
    st.header('')
    
    st.subheader('Race')
    st.altair_chart(satis_race)
    
    
if navigation == 'Income':
    st.subheader('Income')
    st.markdown('Some description')
    st.altair_chart(satis_income)
    st.header('')
    income_navigation = st.selectbox('Choose a survey question to explore by income bracket', (
        'How satisfied are you with Somerville as a place to live?',
        'How satisfied are you with your neighborhood?',
        'Do you feel the City is headed in the right direction or is on the wrong track?',
        'How would you rate the maintenance of streets and sidewalks?',
        'How safe do you feel crossing a busy street in Somerville?',
        'How convenient is it for you to get where you want to go?',
        'How safe do you feel walking in your neighborhood at night?',
        'Age', 'Race', 'Describe your housing status (rent/own)',
        'Do you plan to move away from Somerville in the next two years?', 'Income')) 
    if income_navigation == 'How satisfied are you with Somerville as a place to live?':
        st.altair_chart(income_dropdown_satis)
    if income_navigation == 'How satisfied are you with your neighborhood?':
        st.altair_chart(income_dropdown_neighborhood_satis)
    if income_navigation == 'Do you feel the City is headed in the right direction or is on the wrong track?':
        st.altair_chart(income_dropdown_right_direction)
    if income_navigation == 'How would you rate the maintenance of streets and sidewalks?':
        st.altair_chart(income_dropdown_streets_sidewalks)
    if income_navigation == 'How safe do you feel crossing a busy street in Somerville?':
        st.altair_chart(income_dropdown_street_crossing)
    if income_navigation == 'How convenient is it for you to get where you want to go?':
        st.altair_chart(income_dropdown_convenient_go)
    if income_navigation == 'How safe do you feel walking in your neighborhood at night?':
        st.altair_chart(income_dropdown_safe_at_night)
    if income_navigation == 'Age':
        st.altair_chart(income_dropdown_age)
    if income_navigation == 'Race':
        st.altair_chart(income_dropdown_race)
    if income_navigation == 'Describe your housing status (rent/own)':
        st.altair_chart(income_dropdown_rent_own)
    if income_navigation == 'Do you plan to move away from Somerville in the next two years?':
        st.altair_chart(income_dropdown_moving)

        
if navigation == 'Ward':
    st.subheader('Ward')
    st.markdown('Somerville is divided into seven wards of roughly equal size. Here you can explore how survey results differed by which ward respondent lived in.')
    st.header('')
    st.image('ward map.png')
    st.caption('This map shows average happiness ratings by ward. There was not an appreciable difference in happiness between wards. Ward 5 reported the highest average happiness at 7.6, while its neighbor, Ward 3, reported the lowest average happiness at 7.03. The range in happiness between wards was about half a point')   
    st.header('')
    st.markdown('Average ratings of various aspects of living in Somerville by ward:')
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(ward_housing_cost)
        st.altair_chart(ward_safe_night)
    with col2:
        st.altair_chart(ward_streets_sidewalks)
        st.altair_chart(ward_beauty)
    st.header('')
    st.subheader('Explore survey data by ward:')
    ward_navigation = st.selectbox('Choose a survey question to explore by ward', (
        'How satisfied are you with Somerville as a place to live?',
        'How satisfied are you with your neighborhood?',
        'Do you feel the City is headed in the right direction or is on the wrong track?',
        'How would you rate the maintenance of streets and sidewalks?',
        'How safe do you feel crossing a busy street in Somerville?',
        'How convenient is it for you to get where you want to go?',
        'How safe do you feel walking in your neighborhood at night?',
        'Age', 'Race', 'Describe your housing status (rent/own)',
        'Do you plan to move away from Somerville in the next two years?', 'Income')) 
    if ward_navigation == 'How satisfied are you with Somerville as a place to live?':
        st.altair_chart(ward_dropdown_satis)
    if ward_navigation == 'How satisfied are you with your neighborhood?':
        st.altair_chart(ward_dropdown_neighborhood_satis)
    if ward_navigation == 'Do you feel the City is headed in the right direction or is on the wrong track?':
        st.altair_chart(ward_dropdown_right_direction)
    if ward_navigation == 'How would you rate the maintenance of streets and sidewalks?':
        st.altair_chart(ward_dropdown_streets_sidewalks)
    if ward_navigation == 'How safe do you feel crossing a busy street in Somerville?':
        st.altair_chart(ward_dropdown_street_crossing)
    if ward_navigation == 'How convenient is it for you to get where you want to go?':
        st.altair_chart(ward_dropdown_convenient_go)
    if ward_navigation == 'How safe do you feel walking in your neighborhood at night?':
        st.altair_chart(ward_dropdown_safe_at_night)
    if ward_navigation == 'Age':
        st.altair_chart(ward_dropdown_age)
    if ward_navigation == 'Race':
        st.altair_chart(ward_dropdown_race)
    if ward_navigation == 'Describe your housing status (rent/own)':
        st.altair_chart(ward_dropdown_rent_own)
    if ward_navigation == 'Do you plan to move away from Somerville in the next two years?':
        st.altair_chart(ward_dropdown_moving)
    if ward_navigation == 'Income':
        st.altair_chart(ward_dropdown_income)
    

    
    
if navigation == 'Housing cost':
    st.subheader('Housing cost, housing status, and leaving Somerville')
    st.markdown('Of all the questions on the entire survey, "How would you rate the cost of housing?" is the only one to have an average response below neutral - that is, it is the only area in which Somerville citizens are, on average, very unhappy. Because this issue is such an outlier, we will explore it more in depth here.')
    st.text('')
    st.markdown('Although renters and owners are about equally satisfied with Somerville as a place to live, and although satisfaction with Somerville is a predictor for plans to stay in Somerville, renters have a far higher likelihood of having plans to leave Somerville within the next two years.')
    st.text('')
    col1, colspace, col2 = st.columns([5, 1, 5]) 
    with col1:
        st.altair_chart(rent_own_satis, use_container_width=True)
        st.altair_chart(moving_satis, use_container_width=True)
    with col2:
        st.altair_chart(moving_housing_status_vert)
    st.markdown('What can we learn about who owns and who rents in Somerville, and why people who rent are more likely to leave the city?')
    
    rent_navigation = st.selectbox('Explore how demographic factors are related to housing status (whether people rent or own their homes):', (
        'Income', 'Race', 'Age', 'Survey Language',)) 
    if rent_navigation == 'Income':
        st.altair_chart(rent_income)
    if rent_navigation == 'Race':
        st.altair_chart(rent_race)
    if rent_navigation == 'Age':
        st.altair_chart(rent_age)
    if rent_navigation == 'Survey Language':
        st.altair_chart(rent_language)
        
    moving_navigation = st.selectbox('Explore how demographic factors are related to plans to move away from Somerville in the next two years:', (
        'Income', 'Race', 'Age', 'Living with children under 18',)) 
    if moving_navigation == 'Income':
        st.altair_chart(move_income)
    if moving_navigation == 'Race':
        st.altair_chart(move_race)
    if moving_navigation == 'Age':
        st.altair_chart(move_age)
    if moving_navigation == 'Living with children under 18':
        st.altair_chart(move_children)

    st.header('')

        
        
    
    st.markdown('The question "Do you have plans to move away from Somerville in the next two years?" has a follow-up question on the survey: "If so, why?" This question is completely open-ended; respondents can write anything they like in a blank space. In the word cloud below we can see the overwhelming trend of price and affordability in reasons for leaving Somerville.')
    st.image('wordmap.png')
    
    
    
if navigation == 'Who answered the survey?':
    st.header('Demographic information showing who responded to the survey:')
    st.header('')
    st.subheader('Age')
    st.markdown('Many respondents were 30-40 years old:')
    st.altair_chart(responses_age)
    st.markdown('Select a portion of the right-hand chart to see how many people of each individual age responded to the survey:')
    st.altair_chart(age_bin_brush)
    st.header('')
    st.subheader('Ward')
    st.markdown('The wards were all fairly well-represented:')
    st.altair_chart(responses_ward)
    st.header('')
    st.subheader('Survey Language')
    st.markdown('Most people filled out their surveys in English:')
    st.altair_chart(responses_language)
    st.header('')
    st.subheader('Gender')
    st.markdown('Many respondents were female:')
    st.altair_chart(responses_gender)
    st.header('')
    st.subheader('Race')
    st.markdown('Most respondents were White:')
    st.altair_chart(responses_race)
    st.header('')
    st.subheader('Disability')
    st.markdown('Most respondents did not have a disability:')
    st.altair_chart(responses_disability)
    st.header('')
    st.subheader('Children')
    st.markdown('Most respondents did not live with children:')
    st.altair_chart(responses_children)
    st.header('')
    st.subheader('Housing status')
    st.markdown('Responses were fairly evenly divided between renters and owners:')
    st.altair_chart(responses_rent)
    st.header('')
    st.subheader('Plans to move')
    st.markdown('Most respondents planned to remain in Somerville over the next two years:')
    st.altair_chart(responses_moving)
    st.header('')
    st.subheader('Income')
    st.markdown('There were more responses from the higher income categories:')
    st.altair_chart(responses_income)
    st.header('')
    st.subheader('Students')
    st.markdown('Most respondents were not students:')
    st.altair_chart(responses_student)
    st.header('')
    st.subheader('Residence Length')
    st.markdown('Most respondents had lived in Somerville for less than ten years:')
    st.altair_chart(responses_res_length)
    st.header('')
    st.subheader('Census data shows where the survey oversampled:')
    st.altair_chart(race_census)
    st.altair_chart(responses_race)
    
else:
    pass



    
