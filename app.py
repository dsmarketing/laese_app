import streamlit as st
import google.generativeai as genai

# =========================================================================
# 1. SIDEKONFIGURATION & BØRNEVENLIGT DESIGN (CSS)
# =========================================================================
st.set_page_config(page_title="Min Læse-App", page_icon="📖", layout="centered")

# CSS der styler appen, så den har store knapper og letlæselig tekst på en iPad
st.markdown("""
<style>
    /* Gør alle standardknapper store, grønne og børnevenlige */
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 18px 24px;
        font-size: 16pt !important;
        font-weight: bold;
        border-radius: 16px;
        border: none;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
        transform: translateY(-2px);
    }
    .stButton>button:active {
        transform: translateY(1px);
    }
    /* Gør tekstboksen, hvor historien vises, stor og rar at læse i (børnebogs-stil) */
    .story-text {
        font-size: 18pt !important;
        line-height: 1.7;
        background-color: #fffde7; /* Let gullig papirsfarve, god for øjnene */
        padding: 25px;
        border-radius: 16px;
        border-left: 8px solid #ffeb3b;
        margin-top: 20px;
        margin-bottom: 25px;
        color: #2c3e50;
    }
    /* Gør overskrifter og input-felter en tand større */
    h1 {
        color: #2c3e50;
        font-size: 26pt !important;
    }
    h3 {
        font-size: 16pt !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧙‍♂️ Geminis Magiske Historier")

# =========================================================================
# 2. BRUGERSETTINGS / INDSTILLINGER (I Sidebaren)
# =========================================================================
st.sidebar.header("⚙️ Indstillinger")

alder_trin = st.sidebar.selectbox(
    "Vælg målgruppe (Klassetrin / Alder):",
    options=[
        "Børnehave / 4-5 år (Meget simpelt sprog, helt korte sætninger)",
        "Indskoling (0. - 2. klasse) / 6-8 år (Lix 5-15, korte ord, lydrette ord)",
        "Mellemtrin (3. - 5. klasse) / 9-11 år (Lix 15-25, godt flow, udfordrende ord)",
        "Udskoling (6. - 9. klasse) / 12-15 år (Flot modent sprog)"
    ],
    index=2 # Sætter 3.-5. klasse (Mellemtrin / 9-11 år) som standard
)

historie_type = st.sidebar.selectbox(
    "Historie-genre:",
    options=["Eventyrlig", "Sjov og fjollet", "Spændende mysterium", "Lærerig", "Hyggelig"]
)

# =========================================================================
# 3. BRUGER INPUT & GENERERING
# =========================================================================
st.subheader("📝 Hvad skal historien handle om?")
bruger_input = st.text_area(
    "Skriv stikord, navne eller hvad der skal ske:",
    placeholder="F.eks.: En pige der hedder Sofie, som finder en magisk fodbold, der kan tale...",
    height=120
)

if st.button("Skab historien ✨"):
    if not bruger_input.strip():
        st.warning("Husk lige at skrive et par stikord til historien først! ✍️")
    else:
        # Tjek om Google API-nøglen er sat korrekt i Streamlit Cloud Secrets
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Fejl: API-nøglen blev ikke fundet! Husk at tilføje GOOGLE_API_KEY under 'Secrets' i Streamlit Cloud.")
        else:
            with st.spinner("Gemini brygger på en magisk historie... ✍️"):
                try:
                    # Konfigurer Google AI biblioteket med den hemmelige nøgle
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    
                    # Vi bruger 'gemini-1.5-flash-latest', som løser 404/v1beta-fejlen
                    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
                    
                    # Pædagogisk prompt-opbygning, der tvinger AI til at overholde niveauet
                    full_prompt = (
                        f"Du er en dygtig og erfaren dansk børnebogsforfatter. "
                        f"Skriv en medrivende historie på dansk baseret på disse idéer og stikord: '{bruger_input}'.\n\n"
                        f"Det er ABSOLUT KRITISK, at du tilpasser sproget, sværhedsgraden, ordforrådet og sætningslængden "
                        f"til denne målgruppe: {alder_trin}.\n"
                        f"Historien skal skrives i en {historie_type.lower()} tone, og layoutet skal være overskueligt "
                        f"med luft mellem afsnittene, så den er let at læse for barnet."
                    )
                    
                    # Kald API'en og generer historien
                    response = model.generate_content(full_prompt)
                    
                    # Vis det færdige resultat i den flotte gule læseboks
                    st.success("Så er din historie klar! Rigtig god læselyst! 🎉")
                    st.markdown("---")
                    st.markdown(f"<div class='story-text'>{response.text}</div>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                except Exception as e:
                    st.error(f"Der skete en fejl under kaldet til Gemini: {e}")