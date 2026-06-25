import streamlit as st
import requests

# =========================================================================
# 1. SIDEKONFIGURATION & BØRNEVENLIGT DESIGN (CSS)
# =========================================================================
st.set_page_config(page_title="Min Læse-App", page_icon="📖", layout="centered")

# CSS der styler appen til en iPad (store, farverige knapper og stor skrift)
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
    /* Gør tekstboksen til historien stor og behagelig at læse (børnebogs-stil) */
    .story-text {
        font-size: 18pt !important;
        line-height: 1.7;
        background-color: #fffde7; /* Let gul papirsfarve, som er rar for øjnene */
        padding: 25px;
        border-radius: 16px;
        border-left: 8px solid #ffeb3b;
        margin-top: 20px;
        margin-bottom: 25px;
        color: #2c3e50;
    }
    /* Justering af tekststørrelser */
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
    index=2  # Sætter mellemtrin (9-11 år) som standard
)

historie_type = st.sidebar.selectbox(
    "Historie-genre:",
    options=["Eventyrlig", "Sjov og fjollet", "Spændende mysterium", "Lærerig", "Hyggelig"]
)

# =========================================================================
# 3. BRUGER INPUT & SMART FALLBACK-GENERERING
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
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("Fejl: API-nøglen blev ikke fundet! Husk at tilføje GOOGLE_API_KEY under 'Secrets' i Streamlit Cloud.")
        else:
            with st.spinner("Gemini brygger på en magisk historie... ✍️"):
                
                api_key = st.secrets["GOOGLE_API_KEY"]
                
                # Opbygning af prompten
                full_prompt = (
                    f"Du er en dygtig og erfaren dansk børnebogsforfatter. "
                    f"Skriv en medrivende og færdig historie på dansk baseret på disse idéer: '{bruger_input}'.\n\n"
                    f"Det er ABSOLUT KRITISK, at du tilpasser sproget, sværhedsgraden, ordforrådet og sætningslængden "
                    f"til denne målgruppe: {alder_trin}.\n"
                    f"Historien skal skrives i en {historie_type.lower()} tone. "
                    f"Lav masser af afsnit med god luft imellem, så teksten er visuelt overskuelig for barnet."
                )
                
                payload = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }]
                }
                
                # Liste over mulige modelnavne, som Google accepterer (vi prøver dem fra en ende af)
                modeller_at_teste = [
                    "gemini-2.0-flash",
                    "gemini-1.5-flash-latest",
                    "gemini-1.5-flash",
                    "gemini-1.5-pro"
                ]
                
                forbindelse_succes = False
                sidste_fejlbesked = ""
                
                # Loop igennem modellerne indtil én af dem virker
                for model_navn in modeller_at_teste:
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_navn}:generateContent?key={api_key}"
                        response = requests.post(url, json=payload)
                        response_data = response.json()
                        
                        # Tjek om vi fik et gyldigt tekstsvar retur
                        if 'candidates' in response_data:
                            historie_tekst = response_data['candidates'][0]['content']['parts'][0]['text']
                            
                            st.success("Så er din historie klar! 🎉")
                            st.markdown("---")
                            st.markdown(f"<div class='story-text'>{historie_tekst}</div>", unsafe_allow_html=True)
                            st.markdown("---")
                            
                            forbindelse_succes = True
                            break # Afbryd loopet, da vi har fået vores historie!
                        else:
                            sidste_fejlbesked = str(response_data)
                    except Exception as inner_e:
                        sidste_fejlbesked = str(inner_e)
                
                # Hvis INGEN af modellerne virkede overhovedet
                if not forbindelse_succes:
                    st.error("Kunne ikke oprette forbindelse til nogen af Geminis modeller.")
                    st.write(f"Sidste tekniske svar fra Google: {sidste_fejlbesked}")