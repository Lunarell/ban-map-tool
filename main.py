
import streamlit as st
import pandas as pd

st.set_page_config(page_title="eSports Analyse Tool", layout="wide")

seite = st.sidebar.radio("Seite wählen", ["📥 Match-Erfassung", "📊 Auswertung"])

maps = ["Bank", "Border", "Chalet", "Clubhouse", "Consulate", "Kafe", "Nighthaven", "Oregon", "Skyscraper"]
attack_ops = ["Ace", "Amaru", "Ash", "Blackbeard", "Blitz", "Buck", "Capitao", "Dokkaebi", "Finka", "Flores", "Glaze", "Gridlock", "Hibana", "Iana", "IQ", "Jackal", "Kali", "Lion", "Maverick", "Montagne", "Nokk", "Nomad", "Osa", "Sens", "Sledge", "Thatcher", "Thermite", "Twitch", "Ying", "Zero", "Zofia", "Grim", "Brave", "Fuze", "Ram", "Demos", "Rauora"]
defense_ops = ["Alibi", "Aruni", "Azami", "Bandit", "Castle", "Caveira", "Clash", "Doc", "Echo", "Ela", "Frost", "Goyo", "Jäger", "Kaid", "Kapkan", "Lesion", "Melusi", "Mira", "Mozzie", "Mute", "Orxy", "Pulse", "Rook", "Smoke", "Tachanka", "Thorne", "Thunderbird", "Valkyrie", "Vigil", "Wamai", "Warden", "solis", "Maestro", "Fenrir", "Tubarao", "Skopos"]

if seite == "📥 Match-Erfassung":
    st.title("📥 Match-Erfassung")
    datum = st.date_input("Datum")
    liga = st.text_input("Liga")
    phase = st.selectbox("Phase", ["Playday", "Playoffs", "Runden"])
    team1 = st.text_input("Team 1")
    team2 = st.text_input("Team 2")
    match_format = st.selectbox("Match Format", ["Bo1", "Bo3", "Bo5"])
    faceit_link = st.text_input("Matchlink (Faceit/Desbl)")

    st.subheader("🗺️ Map-Bans & Picks")
    ban_pick_data = []
    if match_format == "Bo1":
        for i in range(8):
            col1, col2 = st.columns(2)
            with col1:
                who = st.selectbox(f"Ban {i+1} von", [team1, team2], key=f"bo1banwho{i}")
            with col2:
                mapname = st.selectbox(f"Map (Ban {i+1})", maps, key=f"bo1banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        pick_team = st.selectbox("Wer pickt die Map?", [team1, team2])
        picked_map = st.selectbox("Welche Map wird gespielt?", maps)
        ban_pick_data.append((pick_team, "Pick", picked_map))
        atk_start = st.selectbox("Start als Attacker", [team1, team2])
        def_start = st.selectbox("Start als Defender", [team1, team2])
    elif match_format == "Bo3":
        for i in range(4):
            st.markdown(f"**Ban {i+1}**")
            who = st.selectbox(f"Wer?", [team1, team2], key=f"bo3banwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo3banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(2):
            st.markdown(f"**Pick {i+1}**")
            who = st.selectbox(f"Wer?", [team1, team2], key=f"bo3pickwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo3pickmap{i}")
            ban_pick_data.append((who, "Pick", mapname))
        for i in range(2):
            st.markdown(f"**Ban {i+5}**")
            who = st.selectbox(f"Wer?", [team1, team2], key=f"bo3banwho2_{i}")
            mapname = st.selectbox("Map", maps, key=f"bo3banmap2_{i}")
            ban_pick_data.append((who, "Ban", mapname))
        who = st.selectbox("Letzter Pick Wer?", [team1, team2])
        mapname = st.selectbox("Letzter Pick Map", maps)
        ban_pick_data.append((who, "Pick", mapname))
    elif match_format == "Bo5":
        for i in range(2):
            who = st.selectbox(f"Ban {i+1} von", [team1, team2], key=f"bo5banwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5banmap{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(2):
            who = st.selectbox(f"Pick {i+1} von", [team1, team2], key=f"bo5pickwho{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5pickmap{i}")
            ban_pick_data.append((who, "Pick", mapname))
        for i in range(2):
            who = st.selectbox(f"Ban {i+3} von", [team1, team2], key=f"bo5banwho2_{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5banmap2_{i}")
            ban_pick_data.append((who, "Ban", mapname))
        for i in range(3):
            who = st.selectbox(f"Pick {i+3} von", [team1, team2], key=f"bo5pickwho2_{i}")
            mapname = st.selectbox("Map", maps, key=f"bo5pickmap2_{i}")
            ban_pick_data.append((who, "Pick", mapname))

    st.subheader("🚫 Operator-Bans pro Map")
    played_maps = [entry[2] for entry in ban_pick_data if entry[1] == "Pick"]
    for m in played_maps:
        st.markdown(f"#### Map: {m}")
        for team in [team1, team2]:
            atk_bans = st.multiselect(f"{team} - Attacker Bans auf {m}", attack_ops, key=f"{team}_{m}_att")
            def_bans = st.multiselect(f"{team} - Defender Bans auf {m}", defense_ops, key=f"{team}_{m}_def")

elif seite == "📊 Auswertung":
    st.title("📊 Match-Auswertung")
    team_filter = st.selectbox("Team auswählen (optional)", ["Alle Teams", "Team 1", "Team 2"])
    st.markdown("### Analyse")
    st.markdown("- Übersicht aller Matches")
    st.markdown("- Welche Maps wurden wie oft gebannt?")
    st.markdown("- Welche Maps wurden wie oft gepickt?")
    st.markdown("- First Ban, Second Ban usw. je Team")
    st.markdown("- Wie viele Runden gewonnen/verloren?")
    st.markdown("- Operator-Bans pro Team und Map")
