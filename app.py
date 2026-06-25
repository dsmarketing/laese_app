import streamlit as st

# Sæt iPad/mobil-venligt layout
st.set_page_config(page_title="Min Læse-App", page_icon="📖", layout="centered")

# CSS til at gøre designet børnevenligt (Store knapper, pæn skrifttype)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 15px 20px;
        font-size: 14pt !important;
        border-radius: 12px;
        border: none;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .story-text {
        font-size: 16pt !important;
        line-height: 1.6;
        background-color: #fffde7;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ffeb3b;
        margin-bottom: 25px;
    }
    .score-box {
        font-size: 12pt;
        font-weight: bold;
        color: #1e88e5;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Initialisering af spil-sessions (holder styr på hvor langt hun er)
if 'page' not in st.session_state:
    st.session_state.page = "start"
if 'xp' not in st.session_state:
    st.session_state.xp = 0

# Scoreboard i toppen
st.markdown(f"<div class='score-box'>⭐ {st.session_state.xp} XP • Læse-Streak: 🔥 1 dag</div>", unsafe_allow_html=True)
st.title("📖 Det Magiske Eventyr")

# Spillets historietræ (Logik)
if st.session_state.page == "start":
    st.markdown("<div class='story-text'>Du står foran en tæt, grøn skov. Solen skinner, men stien deler sig i to. Til venstre hører du den lave lyden af en prustende pony. Til højre glimter noget, der ligner en gylden fodbold bag en busk. Hvad gør du?</div>", unsafe_allow_html=True)
    
    if st.button("A) Gå til venstre mod lyden af ponyen"):
        st.session_state.page = "pony"
        st.session_state.xp += 10
        st.rerun()
        
    if st.button("B) Gå til højre for at undersøge den gyldne fodbold"):
        st.session_state.page = "fodbold"
        st.session_state.xp += 10
        st.rerun()

elif st.session_state.page == "pony":
    st.markdown("<div class='story-text'>Du møder en lille, hvid pony med vinger! Den kigger på dig med store øjne og siger: 'Hjælp mig! En drillesyg ulv har gemt min tryllestav.' Hvad gør du?</div>", unsafe_allow_html=True)
    
    if st.button("A) Led efter ulven i den mørke hule"):
        st.session_state.page = "hule"
        st.session_state.xp += 10
        st.rerun()
    if st.button("B) Tilbyd ponyen et saftigt rødt æble fra din taske"):
        st.session_state.page = "aeble"
        st.session_state.xp += 10
        st.rerun()

elif st.session_state.page == "fodbold":
    st.markdown("<div class='story-text'>Da du rører fodbolden, begynder den at svæve! Den flyver langsomt hen mod en gammel slotsport, som er låst med en stor hængelås. Hvad gør du?</div>", unsafe_allow_html=True)
    
    if st.button("A) Prøv at sparke bolden hårdt mod låsen"):
        st.session_state.page = "spark"
        st.session_state.xp += 10
        st.rerun()
    if st.button("B) Kig under måtten efter en gammel nøgle"):
        st.session_state.page = "noegle"
        st.session_state.xp += 10
        st.rerun()

# Afslutningsskærme (Slutpunkter)
elif st.session_state.page in ["hule", "aeble", "spark", "noegle"]:
    st.markdown(f"<div class='story-text'>Flot læst! Du klarede dette kapitel og nåede en spændende slutning. Du har samlet {st.session_state.xp} magiske point i dag!</div>", unsafe_allow_html=True)
    if st.button("Start et nyt eventyr"):
        st.session_state.page = "start"
        st.rerun()