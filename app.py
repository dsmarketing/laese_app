import streamlit as st
import google.generativeai as genai

# Sæt iPad/mobil-venligt layout
st.set_page_config(page_title="Min Læse-App", page_icon="📖", layout="centered")

# CSS til børnevenligt design (Store knapper, pæn skrifttype)
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
</style>
""", unsafe_allow_html=True)

st.title("🧙‍♂️ Geminis Magiske Historier")

# =========================================================================
# BRUGERSETTINGS / INDSTILLINGER (I Sidebaren)
# =========================================================================
st.sidebar.header("⚙️ Indstillinger")

alder_trin = st.sidebar.selectbox(
    "Vælg målgruppe (Klassetrin / Alder):",
    options=[
        "Børnehave / 4-5 år (Meget simpelt sprog, korte sætninger)",
        "Indskoling (0. - 2. klasse) / 6-8 år",
        "Mellemtrin (3. - 5. klasse) / 9-11 år",
        "Udskoling (6. - 9. klasse) / 12-15 år"
    ],
    index=2 # Sætter 9-11 år (Mellemtrin) som standard
)

historie_type = st.sidebar.selectbox(
    "Historie-genre:",
    options=["Spændende", "Sjov", "Lærerig", "Eventyrlig", "Hyggelig"]
)

# =========================================================================
# BRUGER INPUT
# =========================================================================
st.subheader("📝 Hvad skal historien handle om?")
bruger_input = st.text_area(
    "Skriv stikord eller karakterer:",
    placeholder="F.eks.: En modig hund, der hedder Max, som finder en hemmelig fodboldbane..."
)

if st.button("Skab historien ✨"):
    if not bruger_input.strip():
        st.warning("Husk lige at skrive lidt input først!")
    else:
        # Tjek om Google API-nøglen findes i Streamlit Secrets
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Fejl: API-nøglen blev ikke fundet! Husk at tilføje GOOGLE_API_KEY under 'Secrets' i Streamlit Cloud.")
        else:
            with st.spinner("Gemini skriver på livet løs... ✍️"):
                try:
                    # Konfigurer Google AI med din nøgle
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    
                    # Vi bruger gemini-1.5-flash (lynhurtig og gratis)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Opbyg den pædagogiske prompt
                    full_prompt = (
                        f"Du er en dygtig børnebogsforfatter. Skriv en historie på dansk baseret på disse idéer: '{bruger_input}'.\n\n"
                        f"Det er MEGET vigtigt, at du tilpasser sproget, sværhedsgraden, ordforrådet og sætningslængden "
                        f"til denne målgruppe: {alder_trin}. Historien skal have en {historie_type.lower()} tone."
                    )
                    
                    # Generer tekst
                    response = model.generate_content(full_prompt)
                    
                    st.success("Så er historien klar! 🎉")
                    st.markdown("---")
                    st.markdown(f"<div class='story-text'>{response.text}</div>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                except Exception as e:
                    st.error(f"Der skete en fejl under kaldet til Gemini: {e}")