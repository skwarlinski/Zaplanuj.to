# IMPORTS
import streamlit as st
import pandas as pd
from io import StringIO
from pycaret.clustering import setup, create_model, assign_model, plot_model
import matplotlib.pyplot as plt
import time

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
                placeholder = st.empty()
                with placeholder.container():
                    with st.spinner("Wczytywanie danych..."):
                        time.sleep(3)
                    placeholder.success("✅ Dane zostały wczytane poprawnie!")
                    time.sleep(2)
                placeholder.empty()
            except Exception as e:
                st.error(f"Błąd przy wczytywaniu danych: {e}")
            
        else:
            st.warning("Wprowadź dane przed kliknięciem przycisku.")

# NUM GROUPS INPUT
st.sidebar.subheader("🎯 Dodaj grupy docelowe")
num_groups = st.sidebar.number_input(" Ile grup docelowych chcesz dodać?", min_value=2, max_value=20, step=1)

# CLUSTERING MODEL TRAINING
if df is not None and num_groups:
    try:
        st.subheader("📊 Dane użytkownika do klastrowania")
        st.dataframe(df)

        placeholder = st.empty()
        with placeholder.container():
            with st.spinner(f"Trenuję model z {num_groups} grupami..."):
                time.sleep(3)
            placeholder.success("✅ Model został wytrenowany!")
            time.sleep(2)
        placeholder.empty()

        setup(
            data=df,
            normalize=True,
            verbose=False,
            session_id=42
        )

        model = create_model('kmeans', num_clusters=num_groups)
        clustered_df = assign_model(model)

    
        clustered_df = clustered_df.rename(columns={'Cluster': 'Grupa docelowa'})
        clustered_df["Grupa docelowa"] = clustered_df["Grupa docelowa"].str.replace('Cluster', 'Grupa ')

        st.subheader("📁 Dane użytkownika z przypisanymi klastrami")
        st.dataframe(clustered_df)

        st.subheader("📈 Wizualizacja klastrów")
        plot_model(model, plot='cluster', display_format='streamlit')

    except Exception as e:
        st.error(f"Błąd podczas treningu modelu klastrującego: {e}")