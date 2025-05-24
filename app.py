
# NEUES ESPORTS-ANALYSE WEBTOOL (STREAMLIT)
# Struktur für Login, Dropdown-Menüs, Teamdaten, Map-Auswertung, Operator-Bans

import streamlit as st
import pandas as pd

# Dummy-Login
users = {"admin": "1234", "coach": "abc"}

def login():
    with st.form("Login"):
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        submitted = st.form_submit_button("Einloggen")
        if submitted:
            if users.get(username) == password:
                st.session_state.logged_in = True
                st.session_state.user = username
            else:
                st.error("Login fehlgeschlagen")

# Initialisierung
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    login()
    st.stop()

# --- Hauptdatenstruktur ---
if "matches" not in st.session_state:
    st.session_state.matches = []

# --- Dropdown Optionen ---
maps = ["Oregon", "Bank", "Clubhouse", "Kafe", "Border", "Nighthaven", "Villa", "Chalet", "Skyscraper"]
operators = ["Thatcher", "Thermite", "Ash", "Ying", "Ace", "Sledge", "Smoke", "Mute", "Jager", "Bandit", "Valkyrie", "Mira"]

# --- Match-Eingabe ---
st.title("🎮 Matchdaten eingeben")
with st.form("Match Form"):
    team = st.text_input("Teamname")
    gegner = st.text_input("Gegner")
    format = st.selectbox("Match Format", ["Bo1", "Bo3", "Bo5"])

    st.subheader("Map-Bans (Reihenfolge)")
    map_bans = [st.selectbox(f"Map Ban {i+1}", maps, key=f"ban_{i}") for i in range(5 if format == "Bo1" else (6 if format == "Bo3" else 8))]

    st.subheader("Gespielte Map")
    played_map = st.selectbox("Gespielte Map", maps)
    rounds_won = st.number_input("Runden gewonnen", min_value=0)
    rounds_lost = st.number_input("Runden verloren", min_value=0)

    st.subheader("Operator Bans")
    attacker_bans = [st.selectbox(f"Attacker Ban {i+1}", operators, key=f"att_{i}") for i in range(3)]
    defender_bans = [st.selectbox(f"Defender Ban {i+1}", operators, key=f"def_{i}") for i in range(3)]

    submit = st.form_submit_button("Speichern")
    if submit:
        st.session_state.matches.append({
            "team": team,
            "gegner": gegner,
            "format": format,
            "map_bans": map_bans,
            "played_map": played_map,
            "rounds_won": rounds_won,
            "rounds_lost": rounds_lost,
            "attacker_bans": attacker_bans,
            "defender_bans": defender_bans
        })
        st.success("Match gespeichert!")

# --- Analyse ---
st.title("📊 Matchübersicht & Analyse")
all_data = pd.DataFrame(st.session_state.matches)

# Team-Auswahl
teams = all_data["team"].unique().tolist()
selected_team = st.selectbox("Team auswählen", ["Alle Teams"] + teams)

if selected_team != "Alle Teams":
    data = all_data[all_data["team"] == selected_team]
else:
    data = all_data

# Übersicht
st.subheader(f"Daten {'von ' + selected_team if selected_team != 'Alle Teams' else 'aller Teams'}")
st.write(data)

# Map-Statistik
if not data.empty:
    st.subheader("📍 Meistgespielte Maps")
    map_stats = data["played_map"].value_counts().reset_index()
    map_stats.columns = ["Map", "Gespielt"]
    st.bar_chart(map_stats.set_index("Map"))

    st.subheader("📈 Rundenscore pro Map")
    round_data = data.groupby("played_map")[["rounds_won", "rounds_lost"]].sum()
    st.bar_chart(round_data)

    st.subheader("🧠 Operator Bans (gesamt)")
    attacker_all = pd.Series([op for bans in data["attacker_bans"] for op in bans])
    defender_all = pd.Series([op for bans in data["defender_bans"] for op in bans])
    st.write("**Angreifer Bans:**")
    st.bar_chart(attacker_all.value_counts())
    st.write("**Verteidiger Bans:**")
    st.bar_chart(defender_all.value_counts())
