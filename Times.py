import streamlit as st
from pynytimes import NYTAPI


api_key = "Frvpakmi7RzBNtGrwxKbcGNxwqBNvVEI"
nyt = NYTAPI(api_key, parse_dates=True)

#App theme
light = '''
<style>
    "font-family:georgia;"
</style>'''
st.markdown(light, unsafe_allow_html=True)
st.session_state.theme = "light"

# Apply the theme to the app
st.markdown(light, unsafe_allow_html=True)

st.title("New York Times Stories Sentiment Analysis")

top_stories = nyt.top_stories()
#Grab the first data item in top_stories and view it

#Collecting top stories list
top_story = top_stories

#Getting list of section from the top story dictonary for creating the drop down menu.
section=set()
for ts in top_story:
    sec=str(ts["section"]).upper()
    section.add(sec)
    
option = st.selectbox(
    'Select the section Top Stories',
    (section))

#Getting the stories from certain section
stories=[]
for ts in top_story:
    sec=str(ts["section"]).upper()
    if sec==option:
        stories.append(ts)

#Getting list of stories title from the top story dictonary for creating the drop down menu.
title=[]
for ts in stories:
    titl=str(ts["title"]).upper()
    title.append(titl)

#Checkbox for the top stories title    
for titl in title:    
    st.checkbox(titl)

cols1,cols2=st.columns(2)

ts_keys=[]

for  key_val in stories[0].keys():
    ts_keys.append(key_val)
    
ts_key_removed=['section','subsection','title']    
ts_keys=ts_keys-ts_key_removed
st.write(ts_keys)

with cols2:
    st.write("cols2")

with cols1:
    st.write("cols1")



