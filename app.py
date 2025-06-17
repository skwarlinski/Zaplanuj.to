# IMPORTS
import json
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import pandas as pd
from io import StringIO
from pycaret.clustering import setup, create_model, assign_model, plot_model
import matplotlib.pyplot as plt
import time
from openai import OpenAI 
from dotenv import dotenv_values
import os 

# PAGE CONFIG
st.set_page_config(
    page_title="Zaplanuj.to",
    page_icon="🚶‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# LOTTIE ANIMATIONS
@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_a1 = load_lottiefile("lottie/a1.json")
lottie_a2 = load_lottiefile("lottie/a2.json")
lottie_a3 = load_lottiefile("lottie/a3.json")
lottie_a4 = load_lottiefile("lottie/a4.json")
lottie_a5 = load_lottiefile("lottie/a5.json")
lottie_a6 = load_lottiefile("lottie/a6.json")

# MENU                          
selected = option_menu(
    menu_title="Zaplanuj.to",
    options=["Główna", "Generator", "Kontakt"],
    icons=["house-door", "power", "envelope-at"],
    menu_icon="person-walking",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "1rem 1rem", "background-color": "#0e1117"},
        "icon": {"color": "#007bff"},
        "menu-icon": {"color": "#D8D8D8", "font-size": "1.5rem"},
        "nav-link": {"font-size": "1.2rem", "text-align": "left"},
        "nav-link-selected": {"background-color": "#001e3d"},
        "menu-title": {
            "color": "#007bff",
            "font-size": "42px",
            "font-weight": "bold",
            "width": "100%",
            "text-align": "center",
            "margin": "auto"}
    }
)

# ---MAIN PAGE---
if selected == "Główna":
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🚶‍♂️ Zaplanuj.to - Generator kampanii marketingowych")
        st.markdown("""
        Witaj w Zaplanuj.to! To narzędzie pomoże Ci w tworzeniu i zarządzaniu kampaniami reklamowymi.
        Wybierz opcję "Generator" z menu, aby rozpocząć. Wprowadź dane swojej kampanii, a ja zajmę się resztą. W razie problemów zapraszam do zakładki "Kontakt", gdzie znajdziesz informacje, jak się ze mną skontaktować.
        """)
    
    with col2:
        st_lottie(lottie_a1, speed=1, width=370, height=370, key=None, quality="medium", loop=True, reverse=False)
    
    st.markdown("""---""")

    col1, col2 = st.columns(2)

    with col1:
        st_lottie(lottie_a2, speed=1, width=370, height=370, key=None, quality="medium", loop=False, reverse=False)

    with col2:
        st.header("❓ Jak działa generator?")
        st.markdown("Wystarczy, że wprowadzisz dane swojej kampanii, a ja zajmę się resztą. Możesz przesłać plik CSV lub wkleić dane ręcznie. Następnie wybierz liczbę grup docelowych, a ja wytrenuję model klastrowania i przypiszę użytkowników do odpowiednich grup. Na koniec zobaczysz wizualizację klastrów.")

    st.markdown("""---""")

    col1, col2 = st.columns(2)

    with col1:
        st.header("🧠 Co dzieje się pod maską?")
        st.markdown("""
        Używam algorytmów uczenia maszynowego (takich jak K-means), aby:
        - analizować dane użytkowników,
        - znaleźć wzorce w ich zachowaniach lub cechach,
        - pogrupować ich w segmenty, do których dopasujemy działania marketingowe.
        """)
    
    with col2:
        st_lottie(lottie_a3, speed=100, width=420, height=420, key=None, quality="medium", loop=True, reverse=False)



# ---GENERATOR PAGE---
# FILE UPLOAD OR MANUAL INPUT
if selected == "Generator":
    
    st.sidebar.subheader("Wczytaj dane kampanii")
    data_source = st.sidebar.radio("Wybierz metodę przesyłania danych:", ["📁 Prześlij plik CSV", "📋 Wklej dane ręcznie"] )

    df = None

    if data_source == "📁 Prześlij plik CSV":
        uploaded_file = st.file_uploader("Prześlij plik CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                with st.sidebar:
                    with st.spinner("Wczytywanie danych..."):
                        time.sleep(3)
            except Exception as e:
                st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")

    elif data_source == "📋 Wklej dane ręcznie":
        raw_text = st.text_area("Wklej dane CSV (z nagłówkiem)", height=200, placeholder="przyklad : \nimie,wartosc\nAnna,100\nJan,200")

        if st.button("Wczytaj dane"):
            if raw_text.strip():
                try:
                    df = pd.read_csv(StringIO(raw_text))
                    with st.sidebar:
                        with st.spinner("Wczytywanie danych..."):
                            time.sleep(3)
                except Exception as e:
                    st.error(f"Błąd przy wczytywaniu danych: {e}")
                    
            else:
                st.warning("Wprowadź dane przed kliknięciem przycisku.")

    # NUM GROUPS INPUT
    st.sidebar.subheader("Dodaj grupy docelowe")
    num_groups = st.sidebar.number_input(" Ile grup docelowych chcesz dodać?", min_value=2, max_value=20, step=1)

    # CLUSTERING MODEL TRAINING
    if df is not None and num_groups:
        try:
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Twoje dane", icon="📄"):
                    st.dataframe(df)

            with st.sidebar:
                with st.spinner(f"Trenuję model z {num_groups} grupami..."):
                    time.sleep(3)

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

            with col2:
                with st.expander("Twoje dane z przypisanymi grupami", icon="📁"):
                    st.dataframe(clustered_df)


            with st.sidebar:
                with st.spinner("Generuję wizualizację grup docelowych..."):
                    time.sleep(3)

            col1, col2 = st.columns(2)

            with col1:
                with st.expander("Wizualizacja grup docelowych", icon="📈"):
                    plot_model(model, plot='cluster', display_format='streamlit')

            with st.sidebar:
                with st.spinner("Generuję wykres rozkładu grup docelowych..."):
                    time.sleep(3)

            with col2:
                with st.expander("Wizualizacja rozkładu grup docelowych", icon="📊"):
                    plt.figure(figsize=(10, 6))
                    clustered_df['Grupa docelowa'].value_counts().plot(kind='bar', color='skyblue')
                    plt.title('Liczba użytkowników w poszczególnych grupach docelowych')
                    plt.xlabel('Grupa docelowa')
                    plt.ylabel('Liczba użytkowników')
                    st.pyplot(plt)

            col1, col2, col3 = st.columns(3)

            with col2:
                st.lottie(lottie_a6, speed=1, width=150, height=150, key=None, quality="medium", loop=True, reverse=False)

            # GROUP DESCRIPTIONS (TEXT-TO-TEXT)
            env = dotenv_values(".env")
            openai_client = OpenAI(api_key=env["openai_api_key"])
            if not openai_client.api_key:
                st.error("Nie znaleziono klucza API OpenAI.")
                st.stop()
            def generate_group_descriptions(group_df, nr_group):
                description_stat = group_df.describe(include='all').to_string()
                prompt = f"""
            Jesteś specjalistą ds. marketingu. Oto dane statystyczne użytkowników z grupy {nr_group}:
            {description_stat}

            Na podstawie tych danych:
            1. Wymyśl nazwę tej grupy (króka, chwytliwa, marketingowa).
            2. Napisz krótki opis (2-3 zdania), czym się ta grupa charakteryzuje.
            
            Zwróć odpowiedź w formacie:
            NAZWA: ...
            OPIS: ...
                """
                
                try:
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        temperature=0,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    st.error(f"Błąd generowania opisu: {e}")

            st.subheader("📝 Propozycja nazw i opisów grup docelowych")

            for group in sorted(clustered_df["Grupa docelowa"].unique()):
                group_df = clustered_df[clustered_df["Grupa docelowa"] == group].drop(columns=["Grupa docelowa"])
            
                with st.sidebar:
                    with st.spinner(f"Generuję nazwę i opis dla {group}..."):
                        time.sleep(2)
                text = generate_group_descriptions(group_df, group)

                if "OPIS" in text:
                    name_part, description_part = text.split("OPIS:", 1)
                    name = name_part.replace("NAZWA:", "").strip()
                    description = description_part.strip()
                else:
                    name = ""
                    description = text.strip()
                        
                with st.expander(f"{group}", icon="👥"):    
                    name = st.text_input("Nazwa:", value=name, key=f"name_{group}")
                    description = st.text_area("Opis:", value=description, height=150, key=f"description_{group}")
        
        except Exception as e:
            st.error(f"Błąd podczas treningu modelu: {e}")


# ---CONTACT PAGE---
if selected == "Kontakt":
    
    contact_form = """
    <form action="https://formsubmit.co/skwarlinskihubert@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Imię" required>
        <input type="email" name="email" placeholder="Email" required>
        <textarea name="message" placeholder="Wiadomość" required></textarea>
        <button type="submit">Send</button>
    </form>"""

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

    local_css("style/style.css")
    
    col1, col2 = st.columns(2)

    with col1:
        st_lottie(lottie_a5, speed=1, width=470, height=270, key=None, quality="medium", loop=True, reverse=False)

    with col2:
        st.header("👋 O mnie")
        st.markdown("Nazywam się Hubert Skwarliński i tworzę aplikacje z wykorzystaniem Python/Streamlit. Interesuję się analizą danych, machine learningiem i automatyzacją zadań. Z chęcią podejmę współpracę lub odpowiem na pytania!")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col4:
        st.markdown("""
        <div style="text-align: center;">
        <a href="https://github.com/skwarlinski" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Badge">
        </a>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div style="text-align: center;">
        <a href="https://www.linkedin.com/in/hubert-skwarlinski-895437368/" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge">
        </a>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div style="text-align: center;">
        <a href="mailto:skwarlinskihubert@gmail.com" target="_blank">
            <img src="https://img.shields.io/badge/E--mail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email Badge">
        </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""---""")
        
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📬 Kontakt")
        st.markdown("Jeśli masz pytania lub potrzebujesz pomocy, skontaktuj się ze mną:")
        st.markdown(contact_form, unsafe_allow_html=True)

    with col2:
        st_lottie(lottie_a4, speed=1, width=400, height=400, key=None, quality="medium", loop=False, reverse=False)

    st.markdown("""---""")

    with st.expander("Zależności użyte w projekcie", icon="🧰"):
        st.write("""
        Poniżej znajduje się lista bibliotek i modułów użytych w aplikacji **Zaplanuj.to**, wraz z krótkim opisem ich roli:
        - **streamlit** – główny framework do budowy interfejsu aplikacji webowej w Pythonie.
        - **pandas** – do wczytywania i przetwarzania danych z pliku CSV lub z danych wklejonych ręcznie.
        - **pycaret[clustering]** – do automatycznego tworzenia i trenowania modelu klastrowania (np. KMeans), przypisywania grup i tworzenia wizualizacji.
        - **matplotlib** – biblioteka do tworzenia wykresów, wykorzystywana przez `pycaret` do generowania wykresu klastrów.
        - **streamlit-option-menu** – umożliwia tworzenie niestandardowego menu nawigacyjnego (z ikonami i poziomym układem).
        - **streamlit-lottie** – do odtwarzania animacji `.json` w formacie Lottie, co uatrakcyjnia interfejs.
        - **json** – do wczytywania plików animacji `.json`.
        - **requests** – może być używany do pobierania animacji z internetu (niezastosowany w aktualnym kodzie, ale zaimportowany).
        - **time** – do tworzenia opóźnień i symulacji ładowania (np. podczas wczytywania danych lub trenowania modelu).
        - **io.StringIO** – konwersja tekstu z pola tekstowego do formatu pliku do odczytu przez pandas.
        """)