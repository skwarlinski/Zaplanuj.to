# 📈 Zaplanuj.to – Generator Kampanii Marketingowych

**Zaplanuj.to** to aplikacja webowa oparta na **Streamlit**, która automatyzuje tworzenie kampanii marketingowych na podstawie danych klientów. Wykorzystuje klasteryzację danych (machine learning) oraz model językowy OpenAI, by pomóc marketerom i analitykom w generowaniu spersonalizowanych komunikatów reklamowych dopasowanych do segmentów klientów.

![Streamlit App](https://img.shields.io/badge/built%20with-Streamlit-blue)
![OpenAI](https://img.shields.io/badge/powered%20by-GPT--4o-green)
![License](https://img.shields.io/github/license/skwarlinski/zaplanuj-to)

---

## 🚀 Funkcje

🔹 Wczytaj dane klientów z pliku CSV  
🔹 Zastosuj **klasteryzację (unsupervised learning)** do segmentacji użytkowników  
🔹 Wygeneruj **komunikaty reklamowe dopasowane do każdego segmentu** (grupy docelowej)  
🔹 Edytuj nazwy i opisy grup według własnego uznania  
🔹 Pobierz wyniki jako plik CSV  
🔹 Nowoczesny, responsywny interfejs z animacjami Lottie  
🔹 Wbudowany formularz kontaktowy i portfolio autora

---

## 🧠 Technologie

| Narzędzie | Zastosowanie |
|--|--|
| `Streamlit` | Interfejs webowy |
| `PyCaret` | Klasteryzacja danych |
| `OpenAI API (GPT-4o)` | Generowanie opisów i komunikatów |
| `Pandas / scikit-learn` | Analiza i transformacja danych |
| `dotenv` | Przechowywanie klucza API |
| `Lottie` | Animacje UI |

---

## 🖥️ Demo

> Możesz uruchomić aplikację lokalnie lub na [Streamlit Cloud](https://streamlit.io/cloud).

### 🔧 Instalacja lokalna

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/skwarlinski/zaplanuj-to.git
cd zaplanuj-to

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Ustaw klucz OpenAI w pliku .env

# 4. Uruchom aplikację
streamlit run app.py
```
---

## 📬 Kontakt

Masz pytania lub sugestie? Odezwij się!

- 💼 [LinkedIn](https://www.linkedin.com/in/hubert-skwarlinski-895437368/)
- 💻 [GitHub](https://github.com/skwarlinski)
- ✉️ Email: [skwarlinskihubert@gmail.com](mailto:skwarlinskihubert@gmail.com)

---

## 📜 Licencja

Projekt dostępny na licencji **MIT** – możesz używać, kopiować i rozwijać aplikację na własne potrzeby.
