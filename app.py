import streamlit as st
import requests

API_KEY = "5d072bd163b84870acdcd1e774b499fe"  # pune cheia ta între ghilimele

st.title("Football Stats App ⚽")




ligi = {
    "Premier League":"PL",
    "Serie A": "SA",
    "Laliga" : "PD"
}
option = st.selectbox(
    "What ligue do you want to choose?",
    ("Laliga", "Serie A", "Premier League"),
)
cod = ligi[option]
response = requests.get(
    f"https://api.football-data.org/v4/competitions/{cod}/matches",
    headers= {"X-Auth-Token": API_KEY}
)
date = response.json()



meciuri = date["matches"]
for meci in meciuri[:10]:
    col1, col2 = st.columns(2)
    acasa = meci["homeTeam"]["name"]
    deplasare = meci["awayTeam"]["name"]
    competitie = meci["competition"]["emblem"]
    badge_home =meci["homeTeam"]["crest"] 
    badge_away =meci["awayTeam"]["crest"] 
    score_home = meci["score"]["fullTime"]["home"]
    score_away = meci["score"]["fullTime"]["away"]
    with col1:
        st.header(acasa)
        st.title(score_home)
        st.image(badge_home, width=80)
    with col2:
        st.header(deplasare)
        st.title(score_away)
        st.image(badge_away, width=80)

    
st.write(meciuri[0])
