import streamlit as st
import requests
import datetime

API_KEY = "5d072bd163b84870acdcd1e774b499fe"

# --- Dictionaries ---
statuses = { 
    "Finished": "FINISHED",
    "Scheduled": "TIMED",
    "All": "All"
}
ligi = {
    "Premier League": "PL",
    "Serie A": "SA",
    "Laliga" : "PD",}




# --- Functions ---
def construieste_url(cod, cod_status,option_status):
    if option_status == "All":
        url = f"https://api.football-data.org/v4/competitions/{cod}/matches"
    else :
        url = f"https://api.football-data.org/v4/competitions/{cod}/matches?status={cod_status}"
    response = requests.get(url, headers={"X-Auth-Token": API_KEY}) 
    return response

def afiseaza_meci(meci, cod_status, option_status):
    status = meci["status"]

    col1, col2, col3, col4 = st.columns(4)
    acasa = meci["homeTeam"]["shortName"]
    deplasare = meci["awayTeam"]["shortName"]
    competitie = meci["competition"]["emblem"]
    badge_home =meci["homeTeam"]["crest"] 
    badge_away =meci["awayTeam"]["crest"] 
    score_home = meci["score"]["fullTime"]["home"]
    score_away = meci["score"]["fullTime"]["away"]
    
    timp = datetime.datetime.strptime(meci["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
    data_formatata=timp.strftime("%d.%m.%Y")
    if status == cod_status or option_status=="All":
        with col1:
            st.markdown(acasa)
            if(status== "FINISHED"):
                st.title(score_home)
            st.image(badge_home, width=80)
        with col2:
            st.markdown(deplasare)
            if(status== "FINISHED"):
                st.title(score_away)
            st.image(badge_away, width=80)
        with col3:
            st.write(data_formatata)
        with col4:
            st.write(status)
def construieste_url_clasament(cod):
    url = f"https://api.football-data.org/v4/competitions/{cod}/standings"
    response = requests.get(url, headers={"X-Auth-Token": API_KEY})
    return response
def afiseaza_clasament(clasament):

    for echipa in clasament:
        col1, col2, col3, col4, col5, col6, col7,col8 = st.columns([0.5,0.5,4,0.5,0.5,0.5,0.5,0.5]) #ca sa imi fie alineate coloanele trb pus in for
        pozitie = echipa["position"]
        nume = echipa["team"]["shortName"]
        puncte = echipa["points"]
        with col1:
            st.write(f"{pozitie}. ")
        with col2:
            st.image(echipa["team"]["crest"], width=40)
        with col3:
            st.write(nume)
        with col4:
            st.write(echipa["playedGames"])
        with col5:
            st.write(echipa["won"])
        with col6:
            st.write(echipa["draw"])
        with col7:
            st.write(echipa["lost"])
        with col8:
            st.write(puncte)

def construieste_url_echipa(id_echipa):
    url =  f"https://api.football-data.org/v4/teams/{id_echipa}/matches?status=FINISHED"
    response = requests.get(url,headers={"X-Auth-Token": API_KEY} )
    return response


        
      


# --- UI ---
st.title("Football Stats App ⚽")
option_league = st.selectbox(
    "Liga: ",
    ("Laliga", "Serie A", "Premier League"),
)
tab1, tab2, tab3  = st.tabs(["Meciuri", "Clasament", "Predictii"])
cod = ligi[option_league]


response_clasament = construieste_url_clasament(cod)
date_clasament =  response_clasament.json()
clasament = date_clasament["standings"][0]["table"]
st.write(date_clasament)
echipe = [echipa["team"]["shortName"] for echipa in clasament]

with tab1:
    
    option_status = st.selectbox(
    "Status: ",
    ("Finished", "Scheduled", "All")

)
    cod_status = statuses[option_status]
    response = construieste_url(cod, cod_status, option_status)
    date = response.json()
    meciuri = date["matches"]
    for meci in meciuri:
        afiseaza_meci(meci, cod_status, option_status)

with tab2:
    afiseaza_clasament(clasament)
with tab3: 
        echipe = [echipa["team"]["shortName"] for echipa in clasament]
        ID_echipe = {
    echipa["team"]["shortName"] : echipa["team"]["id"] for echipa in clasament
} #extrag numele si le atasez un ID
        #lista cu echipe pt a putea selecta in selectbox
        option_echipa1 = st.selectbox(
            "Prima echipa: ",
            echipe


        )
        option_echipa2 = st.selectbox(
            "A doua echipa: ",
            echipe


        )
        id_echipa1 = ID_echipe[option_echipa1]
        id_echipa2 = ID_echipe[option_echipa2]
        response_echipa1 = construieste_url_echipa(id_echipa1)
        date_echipa1 = response_echipa1.json()
        response_echipa2 = construieste_url_echipa(id_echipa2)
        date_echipa2 = response_echipa2.json()
        st.write(date_echipa1, date_echipa2)
        




