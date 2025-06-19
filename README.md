# 📈 Zaplanuj.to – Generator Kampanii Marketingowych

**Zaplanuj.to** to aplikacja webowa oparta na **Streamlit**, która automatyzuje tworzenie kampanii marketingowych na podstawie danych klientów. Wykorzystuje klasteryzację danych (machine learning) oraz model językowy OpenAI, by pomóc marketerom i analitykom w generowaniu spersonalizowanych komunikatów reklamowych dopasowanych do segmentów klientów.

![Streamlit App](https://img.shields.io/badge/built%20with-Streamlit-blue)
![OpenAI](https://img.shields.io/badge/powered%20by-GPT--4o-green)

---

## 🚀 Funkcje

🔹 Wczytaj dane klientów z pliku CSV lub wklej je ręcznie  
🔹 Zastosuj **klasteryzację (unsupervised learning)** do segmentacji użytkowników  
🔹 Wygeneruj **nazwy i opisy grup docelowych** na podstawie danych  
🔹 Wygeneruj **kampanie reklamowe** dopasowane do każdej grupy (slogan, post, kreacja, kanał)  
🔹 Edytuj wygenerowane **nazwy i opisy** grup według własnego uznania  
🔹 Pobierz każdą kampanię jako **plik PDF**  
🔹 Zobacz **wizualizację grup docelowych** i rozkład liczebności  
🔹 Nowoczesny, responsywny interfejs z **animacjami Lottie**  
🔹 Wbudowany formularz kontaktowy i sekcja portfolio autora

---

## 🧠 Technologie

| Narzędzie | Zastosowanie |
|----------|--------------|
| `Streamlit` | Interfejs webowy aplikacji |
| `PyCaret` | Klasteryzacja danych (np. K-means), analiza, wizualizacja |
| `OpenAI API (GPT-4o)` | Generowanie nazw grup, opisów i kampanii |
| `Pandas` | Wczytywanie i przetwarzanie danych tabelarycznych |
| `matplotlib` | Wizualizacja wyników klastrowania |
| `reportlab` | Eksport kampanii reklamowych do formatu PDF |
| `Lottie` | Animacje UI w formacie JSON |
| `streamlit-option-menu` | Nawigacja aplikacji z ikonami |
| `streamlit-lottie` | Obsługa animacji Lottie w Streamlit |
| `time / io / json` | Pomocnicze funkcje do ładowania, przetwarzania i opóźnień |

---

## 🖥️ Demo

> Możesz uruchomić aplikację lokalnie lub na [Streamlit Cloud](https://zaplanujto.streamlit.app/).

### 🔧 Instalacja lokalna

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/skwarlinski/zaplanuj-to.git
cd zaplanuj-to

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom aplikację
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
