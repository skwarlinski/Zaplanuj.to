# IMPORTS
import streamlit as st
import pandas as pd
from io import StringIO

st.title("Generator marketingowych kampanii")

upload_method = st.radio("Wybierz metodę przesyłania danych:", ["📁 Prześlij plik CSV", "📋 Wklej dane ręcznie"] )

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