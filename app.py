import streamlit as st
from openai import OpenAI

# Sæt iPad/mobil-venligt layout
st.set_page_config(page_title="Min Læse-App", page_icon="📖", layout="centered")

# [Her beholder du bare alt din CSS-styling og sidebar-indstillinger...]

st.title("🧙‍♂️ Den Magiske Historiefortæller")

# Bruger input-felt
bruger_input = st.text_area(
    "Skriv stikord, karakterer eller en lille start på historien:",
    placeholder="F.eks.: En modig hund, der hedder Max..."
)

# Knap til at generere historien
if st.button("Skab historien ✨"):
    if not bruger_input.strip():
        st.warning("Husk lige at skrive lidt input eller nogle stikord først!")
    else:
        # Tjek om API-nøglen overhovedet findes i Streamlit Secrets inden vi kalder
        if "OPENAI_API_KEY" not in st.secrets:
            st.error("Fejl: API-nøglen blev ikke fundet! Husk at tilføje OPENAI_API_KEY under 'Advanced Settings -> Secrets' i Streamlit Cloud.")
        else:
            with st.spinner("AI'en tænker og skriver på livet løs... ✍️"):
                try:
                    # VI OPPRETTER FØRST KLIENTEN HERINDE NU - DET FORHINDRER CRASH VED OPSTART
                    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                    
                    system_instruktion = f"Du er en dygtig forfatter. Skriv til målgruppen: {alder_trin}."
                    bruger_prompt = f"Skriv en historie baseret på: '{bruger_input}'"

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_instruktion},
                            {"role": "user", "content": bruger_prompt}
                        ],
                        temperature=0.7
                    )
                    
                    historie_resultat = response.choices[0].message.content
                    st.success("Så er historien klar! 🎉")
                    st.markdown("---")
                    st.write(historie_resultat)
                    st.markdown("---")
                    
                except Exception as e:
                    st.error(f"Der skete en fejl under API-kaldet: {e}")