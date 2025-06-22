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
import datetime
from openai import OpenAI 
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth

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

lottie_a1 = load_lottiefile("images/a1.json")
lottie_a2 = load_lottiefile("images/a2.json")
lottie_a3 = load_lottiefile("images/a3.json")
lottie_a4 = load_lottiefile("images/a4.json")
lottie_a5 = load_lottiefile("images/a5.json")

# ---API INPUT---
def verify_api_key(key: str) -> bool:
    try:
        openai_client = OpenAI(api_key=key)
        openai_client.models.list()
        return True
    except Exception:
        return False
    
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = ""
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False


if not st.session_state["openai_api_key"]:

    col1, col2, col3 = st.columns(3)
    with col2:
        with st.form("login_form"):
            user_api_key = st.text_input("🔑 Podaj swój klucz OpenAI API:", type="password")
            submit_user = st.form_submit_button("Zatwierdź")

            if submit_user:
                if user_api_key:
                    if verify_api_key(user_api_key):
                        st.session_state["openai_api_key"] = user_api_key
                        st.success("✅ Klucz API poprawny.")
                        time.sleep(3)
                        st.rerun()
                    else:
                        st.error("❌ Nieprawidłowy klucz API.")
                else:
                    st.warning("⚠️ Wprowadź swój klucz API.")
        
        with st.expander("🔐 Logowanie administratora"):
            with st.form("admin_login_form"):
                admin_user = st.text_input("👤 Login")
                admin_pass = st.text_input("🔒 Hasło", type="password")
                submit_admin = st.form_submit_button("Zaloguj")

                if submit_admin:
                    admin_username = st.secrets["admin"]["username"]
                    admin_password = st.secrets["admin"]["password"]

                    if admin_user == admin_username and admin_pass == admin_password:
                        st.session_state["openai_api_key"] = st.secrets["openai_api_key"]
                        st.session_state["is_admin"] = True
                        st.success("✅ Zalogowano jako administrator.")
                        time.sleep(3)
                        st.rerun()
                    else:
                        st.error("❌ Nieprawidłowe dane.")
        st.stop()
 
# ---MENU---
def show_user_role():
    role = "Administrator" if st.session_state.get("is_admin", False) else "Użytkownik"
    st.markdown(
        f"<div style='position: absolute; top: 0px; right: 5px; font-size: 11px; color: gray;'>"
        f"Tryb: {role}</div>",
        unsafe_allow_html=True
    )

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
    show_user_role()
    
    col1, col2 = st.columns([1, 1], gap="small", vertical_alignment="center")
    
    with col1:
        st.markdown("""
        <div style="
            background-color: rgba(255, 255, 255, 0.02); 
            border-radius: 10px; 
            padding: 30px; 
            margin: auto;
            width: 90%;
            max-width: 600px;
            text-align: left;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <h2 style="margin-bottom: 10px;">🚶‍♂️ Zaplanuj.to – Generator kampanii marketingowych</h2>
            <p>Witaj w Zaplanuj.to! To narzędzie pomoże Ci w tworzeniu i zarządzaniu kampaniami reklamowymi.</p>
            <p>Wybierz opcję <strong>„Generator”</strong> z menu, aby rozpocząć. Wprowadź dane swojej kampanii, a ja zajmę się resztą.</p>
            <p>W razie problemów zapraszam do zakładki <strong>„Kontakt”</strong>, gdzie znajdziesz informacje, jak się ze mną skontaktować.</p>
        </div>
        """, unsafe_allow_html=True)

    
    with col2:
        st_lottie(lottie_a1, speed=1, width=1000, height=500, key=None, quality="medium", loop=True, reverse=False)
    
    st.markdown("""---""")

    col1, col2 = st.columns([1, 1], gap="small", vertical_alignment="center")

    with col1:
        st_lottie(lottie_a2, speed=1, width=1000, height=500, key=None, quality="medium", loop=False, reverse=False)

    with col2:
        st.markdown("""
        <div style="
            background-color: rgba(255, 255, 255, 0.02); 
            border-radius: 10px; 
            padding: 30px; 
            margin: auto;
            width: 90%;
            max-width: 600px;
            text-align: left;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <h2 style="margin-bottom: 10px;">❓ Jak działa generator?</h2>
            <p>Krok po kroku:</p>
            <ol>
                <li><strong>Wprowadź dane kampanii</strong> – przez przesłanie pliku CSV lub ręczne wklejenie danych.</li>
                <li><strong>Określ liczbę grup docelowych</strong>, jakie chcesz wygenerować.</li>
                <li><strong>Podaj cel kampanii reklamowej</strong>, np. zwiększenie sprzedaży lub świadomości marki.</li>
                <li>Aplikacja <strong>wytrenuje model klastrowania</strong> (K-means), który przypisze użytkowników do segmentów.</li>
                <li>Model językowy (GPT) <strong>wygeneruje nazwy i opisy grup docelowych</strong>, które możesz edytować.</li>
                <li>Dla każdej grupy powstanie <strong>spersonalizowana kampania reklamowa</strong> – z hasłem, postem, propozycją grafiki i medium.</li>
                <li>Każdą kampanię możesz <strong>pobrać jako plik PDF</strong>.</li>
            </ol>
            <p>Wszystko w jednym miejscu – szybko, intuicyjnie i z pomocą AI!</p>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("""---""")

    col1, col2 = st.columns([1, 1], gap="small", vertical_alignment="center")

    with col1:
        st.markdown("""
        <div style="
            background-color: rgba(255, 255, 255, 0.02); 
            border-radius: 10px; 
            padding: 30px; 
            margin: auto;
            width: 90%;
            max-width: 600px;
            text-align: left;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <h2 style="margin-bottom: 10px;">🧠 Co dzieje się pod maską?</h2>
            <p>Aplikacja wykorzystuje algorytmy uczenia maszynowego (np. <strong>K-means</strong>) oraz modele językowe (GPT), aby:</p>
            <ul>
                <li><strong>Analizować dane użytkowników</strong> wczytane z pliku CSV lub wprowadzone ręcznie,</li>
                <li><strong>Identyfikować ukryte wzorce</strong> w cechach lub zachowaniach użytkowników,</li>
                <li><strong>Tworzyć grupy docelowe</strong> (segmenty) na podstawie podobieństw,</li>
                <li><strong>Generować nazwy i opisy tych grup</strong> z pomocą AI,</li>
                <li><strong>Dopasować gotowe kampanie reklamowe</strong> do każdej z grup – w tym slogany, posty, propozycje kreacji i kanałów komunikacji.</li>
            </ul>
            <p>Cały proces jest zautomatyzowany, ale użytkownik ma możliwość edycji nazw, opisów oraz ponownego wygenerowania kampanii według własnych preferencji.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st_lottie(lottie_a3, speed=100, width=1000, height=500, key=None, quality="medium", loop=True, reverse=False)



# ---GENERATOR PAGE---
if selected == "Generator":
    show_user_role()
    
    st.sidebar.subheader("1. Wczytaj dane kampanii")
    data_source = st.sidebar.radio("Wybierz metodę przesyłania danych:", ["📁 Prześlij plik CSV", "📋 Wklej dane ręcznie"] )

    df = None

    if data_source == "📁 Prześlij plik CSV":
        uploaded_file = st.file_uploader("Prześlij plik CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
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

    st.sidebar.subheader("2. Dodaj grupy docelowe")
    num_groups = st.sidebar.number_input(" Ile grup docelowych chcesz dodać?", min_value=2, max_value=20, step=1)

    st.sidebar.subheader("3. Cel kampanii reklamowej")
    campain_goal = st.sidebar.text_area(
        "Wprowadź główny cel kampanii:",
        height=120,
        placeholder="Np. zwiększenie świadomości marki, pozyskanie nowych klientów, zwiększenie sprzedaży produktu..."
    )

    bar = st.sidebar
    if df is not None and num_groups and campain_goal:
        if "start_generation" not in st.session_state:
            st.session_state.start_generation = False

        if bar.button("Generuj kampanie i opisy", type="primary"):
            st.session_state.start_generation = True

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

        st.subheader("📊 Analiza i wizualizacja klastrów")

        col1, col2 = st.columns(2, gap="small")

        with col1:
            with st.expander("📄 Twoje dane (oryginalne)", expanded=False):
                st.dataframe(df)

        with col2:
            with st.expander("📁 Dane z przypisanymi grupami", expanded=False):
                st.dataframe(clustered_df)

        col3, col4 = st.columns(2, gap="small")

        with col3:
            with st.expander("📈 Wizualizacja grup docelowych", expanded=False):
                plot_model(model, plot='cluster', display_format='streamlit')

        with col4:
            with st.expander("📊 Rozkład liczebności grup docelowych", expanded=False):
                plt.figure(figsize=(8, 5))
                clustered_df['Grupa docelowa'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
                plt.title('Liczba użytkowników w grupach')
                plt.xlabel('Grupa docelowa')
                plt.ylabel('Liczba użytkowników')
                plt.tight_layout()
                st.pyplot(plt)

        def generate_group_descriptions(group_df, nr_group):
            description_stat = group_df.describe(include='all').to_string()
            prompt = f"""
            Jesteś specjalistą ds. marketingu. Oto dane statystyczne użytkowników z grupy {nr_group}:
            {description_stat}

            Na podstawie tych danych:
            1. Wymyśl nazwę tej grupy (krótka, chwytliwa, marketingowa).
            2. Napisz krótki opis (2-3 zdania), czym się ta grupa charakteryzuje.

            Zwróć odpowiedź w formacie:
            NAZWA: ...
            OPIS: ...
            """
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        
        summary_data = []

        for group in sorted(clustered_df["Grupa docelowa"].unique()):
            name = st.session_state.get(f"name_{group}", "")
            description = st.session_state.get(f"description_{group}", "")
            summary_data.append({
                "Grupa": group,
                "Nazwa grupy": name,
                "Opis grupy": description
            })

        openai_client = OpenAI(api_key=st.session_state["openai_api_key"])
        
        def generate_campaign(group, name, description):
            prompt = f"""
            Jesteś specjalistą ds. marketingu. Twoim zadaniem jest przygotować kampanię reklamową dopasowaną do grupy docelowej.

            Cel kampanii: {campain_goal}

            Grupa docelowa: {group}
            Nazwa grupy: {name}
            Opis grupy: {description}

            Przygotuj:
            1. Slogan reklamowy (krótki, chwytliwy, max 10 słów)
            2. Treść posta na media społecznościowe (2-3 zdania)
            3. Propozycję kreacji graficznej (opisz jak mogłaby wyglądać reklama: kolorystyka, motyw, bohater itp.)
            4. Propozycję medium reklamy (np. Instagram, TikTok, baner, mailing itp.) i uzasadnienie

            Zwróć odpowiedź w przejrzystym formacie z punktami.
            """
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        
        if st.session_state.start_generation:
            st.markdown("### ✏️ Zweryfikuj nazwy i opisy grup docelowych")

            all_groups = sorted(clustered_df["Grupa docelowa"].unique())
                                
            for group in all_groups:
                group_df = clustered_df[clustered_df["Grupa docelowa"] == group].drop(columns=["Grupa docelowa"])

                name_key = f"name_{group}"
                desc_key = f"description_{group}"

                if name_key not in st.session_state or desc_key not in st.session_state:
                    with st.spinner (f"Generuję opis dla {group}..."):
                        text = generate_group_descriptions(group_df, group)

                    if "NAZWA:" in text and "OPIS:" in text:
                        try:
                            name_part, description_part = text.split("OPIS:", 1)
                            name = name_part.split("NAZWA:", 1)[1].strip()
                            description = description_part.strip()
                        except Exception:
                            name, description = f"Grupa {group}", "Opis niedostępny."
                    else:
                        name = f"Grupa {group}"
                        description = text.strip() or "Brak opisu."

                    st.session_state[name_key] = name
                    st.session_state[desc_key] = description

            if "regenerate_campaigns" not in st.session_state:
                st.session_state["regenerate_campaigns"] = False
            
            for group in all_groups:
                name_key = f"name_{group}"
                desc_key = f"description_{group}"
                campaign_key = f"campaign_{group}"

                with st.expander(f"👥 {group} – Edytuj nazwę i opis", expanded=False):
                    st.session_state[name_key] = st.text_input("Nazwa grupy:", value=st.session_state[name_key], key=f"edit_name_{group}")
                    st.session_state[desc_key] = st.text_area("Opis grupy:", value=st.session_state[desc_key], key=f"edit_desc_{group}", height=120)

            if st.button("💾 Zapisz zmiany", type="secondary"):
                st.session_state.regenerate_campaigns = True
                for group in all_groups:
                    name = st.session_state.get(f"name_{group}", "")
                    description = st.session_state.get(f"description_{group}", "")
                    campaign_key = f"campaign_{group}"

                    with st.spinner(f"Generuję kampanię reklamową dla {group}..."):
                        st.session_state[campaign_key] = generate_campaign(group, name, description)

                st.success(" Zaktualizowano kampanie na podstawie nowych nazw i opisów")    

        st.subheader("📢 Kampanie reklamowe")

        for group in sorted(clustered_df["Grupa docelowa"].unique()):
            name = st.session_state.get(f"name_{group}", "")
            description = st.session_state.get(f"description_{group}", "")
            campaign_key = f"campaign_{group}"

            if campaign_key not in st.session_state:
                with st.spinner(f"Generuję kampanię reklamową dla {group}..."):
                    st.session_state[campaign_key] = generate_campaign(group, name, description)

            campaign = st.session_state[campaign_key]
            with st.expander(f"💡 Kampania reklamowa dla {name} ({group})", expanded=True):
                st.markdown(campaign)

                def export_campaign_to_pdf(title: str, content: str) -> BytesIO:
                        buffer = BytesIO()
                        c = canvas.Canvas(buffer, pagesize=A4)
                        width, height = A4
                        margin_left = 2 * cm
                        margin_top = height - 2 * cm
                        line_height = 14
                        c.setFont("Helvetica-Bold", 16)
                        c.drawString(margin_left, margin_top, title)
                        y = margin_top - 2 * line_height
                        c.setFont("Helvetica", 12)
                        max_width = width - 2 * margin_left
                        lines = []
                        for paragraph in content.split('\n'):
                            line = ""
                            for word in paragraph.split():
                                test_line = f"{line} {word}".strip()
                                if stringWidth(test_line, "Helvetica", 12) < max_width:
                                    line = test_line
                                else:
                                    lines.append(line)
                                    line = word
                            lines.append(line)
                        for line in lines:
                            if y < 2 * cm:
                                c.showPage()
                                y = height - 2 * cm
                                c.setFont("Helvetica", 12)
                            c.drawString(margin_left, y, line)
                            y -= line_height
                        c.save()
                        buffer.seek(0)
                        return buffer
                
                pdf = export_campaign_to_pdf(f"Kampania reklamowa - {name}", campaign)
                st.download_button(
                    label="📥 Pobierz kampanię jako PDF",
                    data=pdf,
                    file_name=f"kampania_{name}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_{group}"
                )

# ---CONTACT PAGE---
if selected == "Kontakt":
    show_user_role()
    
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center", )

    with col1:
        st_lottie(lottie_a5, speed=1, width=700, height=400, key=None, quality="medium", loop=True, reverse=False,)

    with col2:
        st.markdown("""
        <div style="
            background-color: rgba(255, 255, 255, 0.02); 
            border-radius: 10px; 
            padding: 30px; 
            margin: auto;
            width: 90%;
            max-width: 600px;
            text-align: left;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <h2 style="margin-bottom: 10px;">👋 O mnie</h2>
            <p>Nazywam się Hubert Skwarliński i tworzę aplikacje z wykorzystaniem Python/Streamlit. Interesuję się analizą danych, machine learningiem i automatyzacją zadań. Z chęcią podejmę współpracę lub odpowiem na pytania!</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small", vertical_alignment="center")

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
        
    
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    
    with col1:   
        google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd93aIMbCN1nk49Wx4ccbxsAc1jctElw_ZoFNso8_kBZx7w8Q/viewform?embedded=true"

        st.markdown(
            f"""
            <div style="
                margin-top: 15px;
                width: 100%;
                max-width: 400px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            ">
                <iframe src="{google_form_url}" width="100%" height="520px" frameborder="0" style="border:0;" allowfullscreen>
                    Ładowanie…
                </iframe>
            </div>
            """,
            unsafe_allow_html=True
        )



    with col2:
        st_lottie(lottie_a4, speed=1, width=400, height=400, key=None, quality="medium", loop=False, reverse=False)

    st.markdown("""---""")

    with st.expander("Zależności użyte w projekcie", icon="🧰"):
        st.write("""
        Poniżej znajduje się lista bibliotek i modułów użytych w aplikacji **Zaplanuj.to**, wraz z krótkim opisem ich roli:
        - **streamlit** – framework do budowy interfejsu webowego, umożliwiający szybkie tworzenie aplikacji w Pythonie.
        - **pandas** – do wczytywania, przetwarzania i analizy danych z plików CSV lub tekstu wprowadzanego ręcznie.
        - **pycaret[clustering]** – narzędzie do automatycznego trenowania modeli klastrowania (np. K-means), przypisywania grup i generowania wizualizacji.
        - **matplotlib** – biblioteka do tworzenia wykresów i wizualizacji danych, wykorzystywana głównie do wyświetlania wyników klastrowania.
        - **streamlit-option-menu** – pozwala na tworzenie estetycznych i intuicyjnych menu nawigacyjnych z ikonami i układem poziomym.
        - **streamlit-lottie** – do odtwarzania animacji w formacie Lottie, które wzbogacają i uatrakcyjniają interfejs użytkownika.
        - **json** – do ładowania i przetwarzania plików animacji `.json` w formacie Lottie.
        - **requests** – biblioteka do wykonywania zapytań HTTP, potencjalnie używana do pobierania zasobów z internetu (aktualnie zaimportowana, ale nieużywana).
        - **time** – do kontrolowania opóźnień i symulacji ładowania, np. podczas wczytywania danych lub generowania wyników.
        - **io.StringIO** – umożliwia konwersję wprowadzonego tekstu CSV na format czytelny dla pandas jako plik w pamięci.
        - **openai** – interfejs do komunikacji z API OpenAI, wykorzystywany do generowania nazw grup, opisów i kampanii reklamowych.
        - **reportlab** – do tworzenia i eksportu wygenerowanych kampanii reklamowych w formacie PDF.
        """)