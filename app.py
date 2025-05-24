
# Streamlit-basierte eSports Analyse Web-App (Grundstruktur, überarbeitet)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="eSports Analyse Tool", layout="wide")

# --- Seitenkopf ---
st.title("📊 eSports Analyse Tool")
st.subheader("Analyse von Map Bans, Operatoren Bans und Team-Statistiken")

# --- Team-Auswahl ---
col1, col2 = st.columns(2)
with col1:
    team1 = st.text_input("Team 1", placeholder="z.B. Team Alpha")
with col2:
    team2 = st.text_input("Team 2", placeholder="z.B. Team Omega")

# --- Matchformat Dropdown ---
match_format = st.selectbox("Match Format", ["Bo1", "Bo3", "Bo5"])

# --- Maps & Map-Bans ---
map_pool = ["Bank", "Border", "Chalet", "Clubhouse", "Consulate", "Kafe", "Nighthaven", "Oregon", "Skyscraper"]

st.markdown("### 🗺️ Map-Bans")
ban_table = []
ban_counts = {"Bo1": 8, "Bo3": 8, "Bo5": 8}
ban_count = ban_counts[match_format]

for i in range(ban_count):
    col1, col2 = st.columns(2)
    with col1:
        banning_team = st.selectbox(f"Wer bannt Map {i+1}?", [team1, team2], key=f"ban_team_{i}")
    with col2:
        banned_map = st.selectbox(f"Map {i+1} (Ban)", map_pool, key=f"map_ban_{i}")
    ban_table.append({"Ban #": i+1, "Team": banning_team, "Map": banned_map})

# --- Picks für Bo3/Bo5 ---
if match_format in ["Bo3", "Bo5"]:
    st.markdown("### ✅ Picks (nur für Bo3/Bo5)")
    picks = []
    pick_rounds = {"Bo3": 3, "Bo5": 5}[match_format]
    for i in range(pick_rounds):
        col1, col2 = st.columns(2)
        with col1:
            picking_team = st.selectbox(f"Team Pick {i+1}", [team1, team2], key=f"pick_team_{i}")
        with col2:
            picked_map = st.selectbox(f"Map Pick {i+1}", map_pool, key=f"map_pick_{i}")
        picks.append({"Pick #": i+1, "Team": picking_team, "Map": picked_map})

# --- Operator-Bans ---
st.markdown("### 🚫 Operator Bans je Map")
operator_list = ["Ace", "Ash", "Thatcher", "Iana", "Maverick", "Sledge", "Hibana", "Zofia", "Thermite", "Ying"]

def operator_bans_section(map_name):
    st.markdown(f"#### 🛡️ Operator Bans auf {map_name}")
    for team in [team1, team2]:
        st.markdown(f"**{team}**")
        att_bans = st.multiselect(f"{team} - Attacker Bans", operator_list, key=f"{team}_{map_name}_att")
        def_bans = st.multiselect(f"{team} - Defender Bans", operator_list, key=f"{team}_{map_name}_def")

if match_format in ["Bo3", "Bo5"]:
    for pick in picks:
        operator_bans_section(pick["Map"])
else:
    for ban in ban_table:
        operator_bans_section(ban["Map"])

# --- Statistiken zu Teams ---
st.markdown("### 🔍 Team Analyse")
team_to_analyze = st.selectbox("Wähle ein Team zur Analyse", [team1, team2])

if st.button("🔎 Analyse anzeigen"):
    # Platzhalter-Datenstruktur – hier würden echte Daten gezogen oder berechnet werden
    st.markdown(f"**Analyse für {team_to_analyze}**")
    st.markdown("- **Maps am häufigsten gebannt**: Clubhouse, Chalet")
    st.markdown("- **Meist gespielte Map**: Bank")
    st.markdown("- **Win/Loss Gesamt**: 3W - 2L")
    st.markdown("- **Runden gewonnen**: 27")
    st.markdown("- **Runden verloren**: 22")
    st.markdown("- **Operator-Ban-Historie** pro Map folgt hier... (TODO)")
