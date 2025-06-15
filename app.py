# IMPORTS
import streamlit as st
import pandas as pd
from io import StringIO

st.title("Generator marketingowych kampanii")


# FILE UPLOAD OR MANUAL INPUT
st.sidebar.subheader("📊 Wczytaj dane kampanii")
upload_method = st.sidebar.radio("Wybierz metodę przesyłania danych:", ["📁 Prześlij plik CSV", "📋 Wklej dane ręcznie"] )

df = None

if upload_method == "📁 Prześlij plik CSV":
    uploaded_file = st.file_uploader("Prześlij plik CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Dane zostały wczytane poprawnie!")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")

elif upload_method == "📋 Wklej dane ręcznie":
    text_input = st.text_area("Wklej dane CSV (z nagłówkiem)", height=200, placeholder="przyklad : \nimie,wartosc\nAnna,100\nJan,200")

    if st.button("Wczytaj dane"):
        if text_input.strip():
            try:
                df = pd.read_csv(StringIO(text_input))
                st.success("Dane zostały wczytane poprawnie!")
            except Exception as e:
                st.error(f"Błąd przy wczytywaniu danych: {e}")
            
        else:
            st.warning("Wprowadź dane przed kliknięciem przycisku.")

if df is not None:
    st.subheader("🔍 Podgląd danych")
    st.dataframe(df)


# TARGET GROUPS INPUT
st.sidebar.subheader("🎯 Dodaj grupy docelowe")
num_groups = st.sidebar.number_input(" Ile grup docelowych chcesz dodać?", min_value=1, max_value=20, step=1)

if "target_groups" not in st.session_state:
    st.session_state.target_groups = [{} for _ in range(num_groups)]

if len(st.session_state.target_groups) != num_groups:
    st.session_state.target_groups = [{} for _ in range(num_groups)]

st.subheader("📝 Wypełnij dane dla każdej grupy:")

for i in range(num_groups):
    with st.expander(f"Grupa {i + 1}", expanded=True):
        group_name = st.text_input(f"🧑‍🤝‍🧑 Nazwa grupy {i+1}", key=f"name_{i}")
        age_range = st.text_input(f"🎂 Przedział wiekowy {i+1}", key=f"age_{i}")
        interests = st.text_area(f"📚 Zainteresowania {i+1}", key=f"interests_{i}")
        budget = st.number_input(f"💰 Budżet reklamowy {i+1} (zł)", min_value=0, step=100, key=f"budget_{i}")

        st.session_state.target_groups[i] = {
            "Nazwa grupy": group_name,
            "Przedział wiekowy": age_range,
            "Zainteresowania": interests,
            "Budżet": budget
        }

if st.button("✅ Zatwierdź wszystkie grupy"):
    df = pd.DataFrame(st.session_state.target_groups)
    st.success("Grupy docelowe zostały zapisane!")
    st.subheader("📋 Twoje grupy docelowe")
    st.dataframe(df)