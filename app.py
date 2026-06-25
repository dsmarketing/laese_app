import streamlit as st
from openai import OpenAI

# 1. Konfiguration og opsætning af OpenAI-klient
# Sørg for at tilføje din OPENAI_API_KEY i Streamlit Cloud under "Advanced Settings" -> Secrets
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    # Hvis du tester lokalt og bruger en .env fil eller miljøvariabel
    client = OpenAI()

st.title("🧙‍♂️ Den Magiske Historiefortæller")
st.write("Skriv dine idéer, og lad AI'en skrive en skræddersyet historie!")

# =========================================================================
# 2. BRUGERSETTINGS / INDSTILLINGER (I Sidebaren)
# =========================================================================
st.sidebar.header("⚙️ Indstillinger for historien")

# Vælg alder / klassetrin
alder_trin = st.sidebar.selectbox(
    "Vælg målgruppe (Klassetrin / Alder):",
    options=[
        "Børnehave / 4-5 år (Meget simpelt sprog, korte sætninger)",
        "Indskoling (0. - 2. klasse) / 6-8 år",
        "Mellemtrin (3. - 5. klasse) / 9-11 år",
        "Udskoling (6. - 9. klasse) / 12-15 år"
    ],
    index=1 # Sætter indskoling som standard
)

# Valgfri ekstra indstilling: Toneleje
historie_type = st.sidebar.selectbox(
    "Historie-genre:",
    options=["Spændende", "Sjov", "Lærerig", "Eventyrlig", "Hyggelig godnathistorie"]
)

# =========================================================================
# 3. BRUGER INPUT (Historie-idér)
# =========================================================================
st.subheader("📝 Hvad skal historien handle om?")
bruger_input = st.text_area(
    "Skriv stikord, karakterer eller en lille start på historien:",
    placeholder="F.eks.: En modig hund, der hedder Max, som finder en hemmelig hule i skoven..."
)

# Knap til at generere historien
if st.button("Skab historien ✨"):
    if not bruger_input.strip():
        st.warning("Husk lige at skrive lidt input eller nogle stikord først!")
    else:
        with st.spinner("AI'en tænker og skriver på livet løs... ✍️"):
            try:
                # 4. Opbygning af prompten baseret på brugerens valg
                system_instruktion = (
                    f"Du er en dygtig forfatter, der skriver historier til børn og unge. "
                    f"Det er MEGET vigtigt, at du tilpasser sproget, sværhedsgraden, ordforrådet "
                    f"og længden til følgende målgruppe: {alder_trin}. "
                    f"Historien skal have en {historie_type.lower()} tone."
                )
                
                bruger_prompt = (
                    f"Skriv en god historie på dansk baseret på disse idéer:\n"
                    f"'{bruger_input}'\n\n"
                    f"Husk at tilpasse sværhedsgraden til målgruppen: {alder_trin}."
                )

                # 5. API Kald til OpenAI (Vi bruger gpt-4o-mini, da den er lynhurtig og billig)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruktion},
                        {"role": "user", "content": bruger_prompt}
                    ],
                    temperature=0.7 # Lidt kreativitet uden at gå helt amok
                )
                
                # 6. Vis resultatet
                historie_resultat = response.choices[0].message.content
                
                st.success("Så er historien klar! 🎉")
                st.markdown("---")
                st.write(historie_resultat)
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Der skete en fejl under genereringen: {e}")