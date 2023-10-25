import pandas as pd
from connection import MarvelAPIEventConnection
import streamlit as st

st.set_page_config(layout="wide", page_title='Marvel Events Dashboard')

############### define sidebar style ################
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

############### reduce top margin ################
st.markdown(
        """
<style>
    .css-z5fcl4 {
        padding-top: 0px;
    }
</style>
""",
        unsafe_allow_html=True,
    )

############### hidde hamburguer menu ################
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

############### hidde collapse sider button ################
st.markdown(""" <style type="text/css"> 
div.css-1nm2qww {
  display:none;
}
</style>""", unsafe_allow_html=True)

public_key = "SUA_CHAVE_AQUI"
private_key = "SUA_CHAVE_AQUI"

id = []
event_name = []
event_description = []
thumbnail = []
comics_count = []
stories_count = []
series_count = []
characters_count = []

event_conn = st.experimental_connection("marvel_events", type=MarvelAPIEventConnection, public_key=public_key, private_key=private_key
                                        , offset= 0)
event_req = event_conn.get(ttl="2sec")
total_events = event_req['data']['total']

for i in event_req["data"]["results"]:
    id.append(i["id"])
    event_name.append(i["title"])
    event_description.append(i['description'])
    thumbnail.append(i['thumbnail']['path'] + '/portrait_uncanny.jpg')
    comics_count.append(i['comics']['available'])
    stories_count.append(i['stories']['available'])
    series_count.append(i['series']['available'])
    characters_count.append(i['characters']['available'])

a = {"id": id, "event_title": event_name,"event_description": event_description, "event_imag": thumbnail,  "comics_count": comics_count,
     "stories_count": stories_count, "series_count": series_count, "characters_count": characters_count}
df_events = pd.DataFrame.from_dict(a)

def main():
    
########################################################### HOME ##############################################################
    st.subheader('Welcome to Marvel Events page!!')
    st.write('**Currently there are ' + str(total_events) + ' events in marvel universe.**')
    selected_event = st.selectbox('Choose one Marvel event:', sorted(df_events["event_title"].values.tolist()))

    selected_event_id = df_events[df_events['event_title'] == selected_event]['id'].item()
    selected_event_desc = df_events[df_events['event_title'] == selected_event]['event_description'].item()
    selected_event_img = df_events[df_events['event_title'] == selected_event]['event_imag'].item()
    selected_event_comics = df_events[df_events['event_title'] == selected_event]['comics_count'].item()
    selected_event_stories = df_events[df_events['event_title'] == selected_event]['stories_count'].item()
    selected_event_series = df_events[df_events['event_title'] == selected_event]['series_count'].item()
    selected_event_char = df_events[df_events['event_title'] == selected_event]['characters_count'].item()

    st.markdown("<p align='center', style='color:#27add9;font-size:30px;'> <b>This event have</b> </p>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write("")
    with col2:
        st.metric(label="Comics", value=str(selected_event_comics), )            
    with col3:
        st.metric(label="Stories", value=str(selected_event_stories))
    with col4:
        st.metric(label="Series", value=str(selected_event_series))
    with col5:
        st.metric(label="Characters", value=str(selected_event_char))

    st.write("**Event description**")     
    st.write(selected_event_desc)

    ########################################################### SIDEBAR ##############################################################    

    st.sidebar.image(selected_event_img, caption=selected_event)

if __name__ == "__main__":
    main()
