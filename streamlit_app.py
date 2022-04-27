import pandas as pd
import altair as alt
import streamlit as st

happiness_2021 = pd.read_csv('happiness 2021.csv')
cases_per_day = pd.read_csv('cases_per_day.csv')

#merging COVID cases per day with happiness survey results, on date postmarked
happiness_2021['Envelope Postmarked:'] = pd.to_datetime(happiness_2021['Envelope Postmarked:'])
cases_per_day['Test Date'] = pd.to_datetime(cases_per_day['Test Date'])
cases_per_day.rename(columns = {'Test Date':'Envelope Postmarked:'}, inplace = True)
df = happiness_2021.merge(cases_per_day, on = 'Envelope Postmarked:', how = 'left')





#CLEANING AND ORGANIZING DATA

#cleaning open-ended repsonse data - how long have you lived in somerville
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.lower()
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('months', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('month ', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('mon ', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('mon.', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('mo ', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('mo.', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('ms', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('mths', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('meses', 'MONTH', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('1/2', '.5', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace(' ', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('since', 'SINCE', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('1995', 'SINCE 1995', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('+', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('-', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('<', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('>', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('~', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace('*', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.replace(',', '', regex = True)
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].str.strip('abcdefghijklmnopqrstuvwxyz')

def clean_dates(y):
    x = str(y)
    if 'MONTH' in x:
        a = x.replace('MONTH', '')
        return ((float(a))/12)
    elif 'SINCE' in x:
        b = x.replace('SINCE', '')
        return 2021-float(b)
    else: return y
   
df['11. How long have you lived in Somerville?'] = df['11. How long have you lived in Somerville?'].apply(clean_dates)


#cleaning response data - what is your gender
df['1. What is your gender '] = df['1. What is your gender '].str.replace('N', 'n', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('-', '', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace(' ', '', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('nan', '', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('nonbinaryfemme', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Genderqueer', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Transgenderman', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Demifemme', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Genderfluid', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('nonbinary', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Tom', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].str.replace('Agender', 'Gender Non-Conforming', regex = True)
df['1. What is your gender '] = df['1. What is your gender '].replace(to_replace='', value='No Answer')
df['1. What is your gender '].fillna('No Gender Given',inplace=True)

#cleaning response data - what is your age
df['What is your age?'] = df['What is your age?'].str.lower()
df['What is your age?'] = df['What is your age?'].str.replace('+', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace('years', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace('>', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace('/', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace('-70', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace('\'', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.replace(' ', '', regex = True)
df['What is your age?'] = df['What is your age?'].str.strip('abcdefghijklmnopqrstuvwxyz')
df['What is your age?'] = df['What is your age?'].replace(to_replace='', value='No Age Given')
df['What is your age?'] = df['What is your age?'].replace(to_replace='null', value='No Answer')
df['What is your age?'].fillna('No Age Given',inplace=True)

#cleaning data - what languages do you speak at home
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace(',', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('/', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace(' y ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace(' and ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('&', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('2', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('1', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('+', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Purtugues', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Portugues Brazie', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Portugues ', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Portugues (Brasil)', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Portgues', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('english', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Ctt  python', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Ingles', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('ingles', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Eng ', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('german', 'German', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Italiano', 'Italian', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Creol Hatien', 'Kreyol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Creole', 'Kreyol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('russian', 'Russian', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('spanish', 'Spanish', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('espanol', 'Espanol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('french', 'French', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('American', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Chinese Mandarin', 'Chinese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('catalan', 'Catalan', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Haitian Kreyol', 'Kreyol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Cantonese', 'Chinese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Kreyole', 'Kreyol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Cantonses', 'Chinese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('US', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Several', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Sign Language', 'ASL', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Creol  Haitien', 'Kreyol', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('(Brasil)', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('\(\)', '', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Portuguese(Brasil)', 'Portuguese', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Espanol', 'Spanish', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('English', 'Eng', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('Eng', 'English', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('   ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('  ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('   ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace('   ', ' ', regex = True)
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.strip()
df['3. What language(s) do you speak at home?'] = df['3. What language(s) do you speak at home?'].str.replace(' ', ';', regex = True)

#rename columns removing troublesome characters
column_rename_dict = {
    'Envelope Postmarked:': 'postmark_date',
    'Language submitted in:': 'survey_language',
    '1. How happy do you feel right now?': '1_happy_now',
    '2. How satisfied are you with your life in general?': '2_satisfied_life',
    '3. How satisfied are you with Somerville as a place to live?': '3_satisfied_somerville',
    '4. How satisfied are you with your neighborhood?': '4_satisfied_neighborhood',
    '5. Do you feel the City is headed in the right direction or is it on the wrong track?': '5_right_direction',
    '6a. How would you rate the availability of information about city services?': '6a_city_services',
    '6b. How would you rate the cost of housing?': '6b_housing_cost',
    '6c. How would you rate the overall quality of public schools?': '6c_schools',
    '6d. How would you rate your trust in the local police?': '6d_trust_police',
    '6e. How would you rate the maintenance of streets and sidewalks?': '6e_streets_sidewalks',
    '6f. How would you rate the availability of social community events?': '6f_social_events',
    '7. In the past year, have you used 311 (via phone, online, etc)?': '7_use_311',
    '8. In the past year, did you attend a City led meeting?': '8_meeting',
    '9. How safe do you feel crossing a busy street in Somerville?': '9_street_crossing',
    '10. How convenient is it for you to get where you want to go? ': '10_convenient_go',
    '11. How safe do you feel walking in your neighborhood at night?': '11_safe_at_night',
    '12. How satisfied are you with the appearance of parks and squares in your neighborhood?': '12_neighborhood_parks',
    '13. How satisfied are you with the beauty or physical setting of your neighborhood?': '13_neighborhood_beauty',
    '14. How satisfied are you with the condition of your housing?': '14_housing_condition',
    '15. In the past year, how satisfied were you with your ability to access City services?': '15_access_services',
    '1. What is your gender ': 'd1_gender',
    'What is your age?': 'd2_age',
    '3. What language(s) do you speak at home?': 'd3_home_language',
    '4. What is your race or ethnicity?': 'd4_race',
    '5. Do you identify as having a disability and/or physical impairment that substantially limits one or more of your major activities?': 'd5_disability',
    '6. Do you have children age 18 or younger who live with you?': 'd6_children',
    '7. Describe your housing status in Somerville.': 'd7_rent_own',
    '8a. Do you plan to move away from Somerville in the next two years?': 'd8a_moving',
    '8b. If yes, why?': 'd8b_moving_why',
    '9. What is your annual household income?': 'd9_income',
    '10. Are you a student?': 'd10_student',
    '11. How long have you lived in Somerville?': 'd11_residence_length',
    '12. What is your primary mode of transportation? ': 'd12_transportation',
    'Any comments?': 'comments',
    'Confirmed (by PCR) COVID Cases': 'COVID cases'
}
df = df.rename(columns = column_rename_dict)

#comments from open-ended comment field
comments = [
    'Please paint city hall it is a disgrace', 
    'Keep building bike paths!', 
    'PLEASE FIX HIGHLAND ST -- VERY UNSAFE FOR BIKING', 
    'The whites here look @ me & wont even say hi!! (Note: I am black...)', 
    'I\'m tired of attending "affordable housing" meetings and seeing all the foreigners whose income is not considered or they have vouchers. I,  a middle class senior, would have to pay $1,800 for affordable housing. I\'ve lived and worked in Somerville my whole life (74 years). I love Somerville but this is unfair. Low income people take affordable apartments from middle class seniors. They are more important than me. More affordable housing for "middle class seniors" please. ', 
    'Too many rats', 
    'Rats day and night', 
    'When call about drug dealings cops should come!! Also blind spots in the city need to be taken care of. The rats need to be taken care of. I sent in paperwork have not heard back in months. ', 
    'There has been a car on Skehan Street parked years. Tar on entire street is chewed up in chunks. Skehan Street is in disrepair. Needed work and new street years ago. Very bad. ', 
    "Can't we address the homeless situation better?", 
    'WASTE OF MONEY', 
    'There are too many street fairs', 
    'I feel on a cracked sidewalk on Thursday St in January, broke my shoulder and banged knee very bad, called the city about it and got no call back + sidewalk still broken and hazardous. This injury cost me close to $1,000 in medical copays. When will the city fix all upraised cracked sidewalks?', 
    'I am very unsatisfied with my life because I live in Somerville', 
    'Compost!', 
    'I like it here', 
    'I had to pay a bribe to get a building permit. ', 
    "311 hasn't responded to many complaints about a huge rat problem on Belmont Street. ", 
    'a ciudad de somerville e muito cara para viver principalmente ma agua ma suver e mas texes muito dificil esta sempre a subir e a gente a descer e buracos mos carninhos que cabe um cao. daqui sera para o cerritrio. ', 
    'Somerville would be perfect if not for litter + rats! The litter is terrible! The rats are a real problem. ', 
    'Pot holes are unbearable', 
    'The current mayor was good in the beginning, lowering taxes for property owners, but money from developers turned him into an idiot who bows down to the young yuppies who want everything their own way, who want to defund police, and get rid of cars. Bring back the old Somerville', 
    'Thanks for asking', 
    'The problem with somerville is that in the last ten years, its become a city of transient 20-something year olds, packed into small apartments. All the families in my neighborhood have left. No kids, not too many middle aged. Just post-college dorms and absent landlords. ', 
    'I like the city as long as prices do not rise', 
    'What are city services? Trust in local police is better than most.', 
    'We are the Denmark of Middlesex County', 
    'concerned about socialist City Council', 
    'Big rat problem electric ave somerville, help!', 
    'More trees!', 
    "Squares could be cleaner.", 
    'My only complaint are the airplanes that keep waking me up!', 
    'No one stops at crosswalks!', 
    'Travel is getting worse due to all the new bus lanes', 
    'Trash on the sidewalks', 
    'drug users in Davis square all day', 
    'Landlord always evicts me', 
    'often menaced by law-breaking cyclists ', 
    'Summer streets is great. I HATE Porch Fest!!!', 
    'More mature trees!', 
    'more information should be sent via mail, bikes a problem. do not obey laws', 
    'Remove some of the unnessacary Red Lights and tak down the no right on Red signs so we dont polute the environment', 
    'Thanks for ever improving our wonderful city! :)', 
    'We need more on street parking', 
    'Hostile architecture & bad urban planning. Make the sidewalks appropriately aligned w/ traffic', 
    'Loose wires hanging all over the city make people unsafe and obstruct city views ', 
    'This survey is bullshit', 
    'Send a survey w/ specific topics', 
    'Love the trees the city planted', 
    'Don\'t walk at night', 
    'Why don\'t you ask about parking? you put in bike routes (which I rarely see anyone use) and bus routes, which are not frequently used. I can\'t go to some of my usual/favorite shops because of the complete lack of parking now.', 
    'I love apartment housing', 
    'Bring back porch fest!!', 
    'City response to reporting rats not helpful', 
    'Dilboy pool hours horrible, 2+ hours daily to clean pool - joke', 
    'Except for rats!', 
    'Developers are out pricing Artists. Please keep Somerville affordable. Ride share', 
    'WHAT A WASTE OF MY TAX DOLLARS', 
    'How many time do I have to take this survey? This is the second time with in a month', 
    'Tufts, The landlords of student homes on college are do not take care of properties. Students are filthy with porcites and yards', 
    'For health reasons some of us need to be able to get around using cars. For safety reasons-making driving harder makes Somerville less safe for women at night.', 
    'year + school closure has made me loose trust in leadership. wish libraries were open for appts. to browse.', 
    "there's a lot of people in a small area how would we manage a civic emergency, disaster, or critical service interuption? evacuation would be a nightmare. there aren't enough grocery stores in walking distance ~ its just hard to make a plan for resilliency, basically", 
    "Please add speed bumps or signs showing driver's speed on Broadway, Lower East from Sullivan heading toward McGrath.", 
    'I WILL BE HAPPY WHEN BIDEN IS OUT OF OFFICE! THIS GUY AND IDIOT']

#cleaning race/ethnicity data to match census categories
df['d4_race'] = df['d4_race'].str.replace('Hispanic/Latino', 'Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('all of the above', 'Two or More Races, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('U.S citizen', '', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Celtic', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Jewish', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Southern european', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Human Race', '', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Ashkenazi', '', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Caucasian', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Mixed', 'Two or More Races, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Middle Eastern', 'Some Other Race alone, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Albanian/Italian', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Haitian-American', 'Black or African American Alone, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('US Citizen', '', regex = True)
df['d4_race'] = df['d4_race'].str.replace('White / Middle Eastern', 'Two or More Races, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Gaelic', 'White', regex = True)
df['d4_race'] = df['d4_race'].str.replace('Portuguese', 'Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('American Black', 'Black or African American Alone, Not Hispanic or Latino', regex = True)
df['d4_race'] = df['d4_race'].str.replace('lingua portugesa', 'Hispanic or Latino', regex = True)

df['d4_race'] = df['d4_race'].replace(to_replace='White; Some Other Race alone, Not Hispanic or Latino', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='White;Hispanic or Latino', value='Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Asian;White', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Hispanic or Latino;White', value='Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='White;Native American', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Black/African American;White', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Asian;Hispanic or Latino;White', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Hispanic or Latino;White;Moreno', value='Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='White;White', value='White')
df['d4_race'] = df['d4_race'].replace(to_replace='Asian;White;Two or More Races, Not Hispanic or Latino race', value='Two or More Races, Not Hispanic or Latino race')
df['d4_race'] = df['d4_race'].replace(to_replace='Asian;Hispanic or Latino', value='Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='White / Some Other Race alone, Not Hispanic or Latino', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Hispanic or Latino;White;Some Other Race alone, Not Hispanic or Latino', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='Two or More Races, Not Hispanic or Latino race', value='Two or More Races, Not Hispanic or Latino')
df['d4_race'] = df['d4_race'].replace(to_replace='White;', value='White')
df['d4_race'] = df['d4_race'].replace(to_replace='nan', value='No Race Given')
df['d4_race'] = df['d4_race'].replace(to_replace='', value='No Race Given')
df['d4_race'].fillna('No Race Given',inplace=True)
df['d4_race'] = df['d4_race'].replace(to_replace='Black/African American', value='Black or African American Alone, Not Hispanic or Latino')

df['8_meeting'] = df['8_meeting'].replace(to_replace='nan', value='No Answer Given')
df['8_meeting'] = df['8_meeting'].fillna('No Answer Given')
df['7_use_311'] = df['7_use_311'].replace(to_replace='nan', value='No Answer Given')
df['7_use_311'] = df['7_use_311'].fillna('No Answer Given')
df['Ward'] = df['Ward'].replace(to_replace='nan', value='No Answer Given')
df['Ward'] = df['Ward'].fillna('No Answer Given')
df['survey_language'] = df['survey_language'].replace(to_replace='nan', value='No Answer Given')
df['survey_language'] = df['survey_language'].fillna('No Answer Given')
df['survey_language'] = df['survey_language'].str.replace('Portugese', 'Portuguese', regex = True)
df['d2_age'] = df['d2_age'].replace(to_replace='nan', value='No Age Given')
df['d2_age'] = df['d2_age'].fillna('No Age Given')
df['d5_disability'] = df['d5_disability'].replace(to_replace='nan', value='No Answer Given')
df['d5_disability'] = df['d5_disability'].fillna('No Answer Given')
df['d6_children'] = df['d6_children'].replace(to_replace='nan', value='No Answer Given')
df['d6_children'] = df['d6_children'].fillna('No Answer Given')
df['d8a_moving'] = df['d8a_moving'].replace(to_replace='nan', value='No Answer Given')
df['d8a_moving'] = df['d8a_moving'].fillna('No Answer Given')
df['d9_income'] = df['d9_income'].replace(to_replace='nan', value='No Answer Given')
df['d9_income'] = df['d9_income'].fillna('No Answer Given')
df['d10_student'] = df['d10_student'].replace(to_replace='nan', value='No Answer Given')
df['d10_student'] = df['d10_student'].fillna('No Answer Given')

df['d7_rent_own'].fillna('No Answer Given',inplace=True)
df['d7_rent_own'] = df['d7_rent_own'].replace(to_replace="pagando ipoteca (paying mortgage)", value='Own')

#from open-ended question do you plan to move out of somerville - if so, why?
why_move = df['d8b_moving_why'].dropna().tolist()







#HAPPINESS AND SATISFACTION WITH SOMERVILLE AS A PLACE TO LIVE

#overall happiness
overall_happiness = alt.Chart(df).mark_bar(size = 30).encode(
    alt.X('1_happy_now'),
    alt.Y('count()'))
st.altair_chart(overall_happiness, use_container_width=False)
