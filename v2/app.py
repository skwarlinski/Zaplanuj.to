# IMPORTS
import streamlit as st
import pandas as pd
from io import StringIO


st.sidebar.title("Generator marketingowych kampanii")

# FILE UPLOAD OR MANUAL INPUT
st.sidebar.subheader("📊 Wczytaj dane kampanii")
data_source = st.sidebar.radio("Wybierz metodę przesyłania danych:", ["📁 Prześlij plik CSV", "📋 Wklej dane ręcznie"] )

df = None

if data_source == "📁 Prześlij plik CSV":
    uploaded_file = st.file_uploader("Prześlij plik CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Dane zostały wczytane poprawnie!")
        except Exception as e:
            st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")

elif data_source == "📋 Wklej dane ręcznie":
    raw_text = st.text_area("Wklej dane CSV (z nagłówkiem)", height=200, placeholder="przyklad : \nimie,wartosc\nAnna,100\nJan,200")

    if st.button("Wczytaj dane"):
        if raw_text.strip():
            try:
                df = pd.read_csv(StringIO(raw_text))
                st.success("Dane zostały wczytane poprawnie!")
            except Exception as e:
                st.error(f"Błąd przy wczytywaniu danych: {e}")
            
        else:
            st.warning("Wprowadź dane przed kliknięciem przycisku.")

if df is not None:
    st.subheader("🔍 Podgląd danych")
    st.dataframe(df.head())


# TARGET GROUPS INPUT
st.sidebar.subheader("🎯 Dodaj grupy docelowe")
num_groups = st.sidebar.number_input(" Ile grup docelowych chcesz dodać?", min_value=1, max_value=20, step=1)
