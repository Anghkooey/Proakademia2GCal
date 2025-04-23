# Importer ICS do Google Kalendarza: Automatyczny import harmonogramów 📅✨

<p align="center">
  <a href="https://github.com/Anghkooey/uafm_ical/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Anghkooey/uafm_ical?style=for-the-badge" alt="License Badge">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  </a>
  <a href="https://github.com/Anghkooey/uafm_ical/commits/main">
    <img src="https://img.shields.io/github/last-commit/Anghkooey/uafm_ical?style=for-the-badge" alt="Last Commit Badge">
  </a>
</p>

<p align="center">
  <a href="pl.md"><img src="flags/pl_icon.svg" width="70" alt="Polski"></a>
  <a>  </a>
  <a href="README.md"><img src="flags/en_icon.svg" width="70" alt="Angielski"></a>
  <a>  </a>
  <a href="ua.md"><img src="flags/ua_icon.svg" width="70" alt="Ukraiński"></a>
</p>

**Masz dość ręcznego dodawania zajęć do Kalendarza Google? 😩 Ten skrypt w Pythonie zrobi to za Ciebie automatycznie!** **Importuj wydarzenia z pliku ICS (iCalendar) bez żadnego wysiłku — szybko, czysto i inteligentnie. ✨**

**Oryginalnie stworzony dla [Uniwersytetu Andrzeja Frycza Modrzewskiego](https://uafm.edu.pl/), działa z każdym plikiem ICS, również z systemów jak Mobilny Student: [link do planów](https://dziekanat.uafm.edu.pl/Plany/PlanyGrup).**

**✔️ Tworzy kalendarz, jeśli go nie masz  
✔️ Usuwa wydarzenia starsze niż 30 dni  
✔️ Czyści i formatuje plan zajęć profesjonalnie**

## ✨ Kluczowe funkcje

- **Automatyczny import:** Harmonogram z pliku ICS trafia prosto do Twojego Kalendarza Google.
- **Uniwersalna kompatybilność:** Obsługuje pliki ICS z różnych systemów akademickich (APR, Mobilny Student, itd.).
- **Nowy kalendarz:** Jeśli nie podasz ID, stworzy nowy o nazwie "Study".
- **Czysty kalendarz:** Przed importem usuwa stare wydarzenia.
- **Koloryzacja wydarzeń:** Rozróżnia typy zajęć kolorami (Egzaminy ❤️, Wykłady 🖤 itd.).
- **Obsługa stref czasowych:** Wszystko zsynchronizowane ze strefą czasową Twojego kalendarza.

## 🚀 Szybki podgląd

**Zobacz skrypt w akcji! ✨ Animacja pokazuje import planu zajęć do Google Kalendarza.**

<div align="center">
<img src="preview/preview.gif" alt="Podgląd importu ICS" width="600">
</div>

<div align="center">
<h3>🗓️ Widok kalendarza</h3>
</div>

|                      **Przed**                      |                     **Po**                      |
| :-------------------------------------------------: | :---------------------------------------------: |
| ![Before](preview/pictures/calendar_before.png)     | ![After](preview/pictures/calendar_after.png)   |

<div align="center">
  <h3><strong>📝 Widok opisu wydarzenia</strong></h3>
</div>

|                                        **Przed**                                         |                                      **Po**                                      |
| :--------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| <img src="preview/pictures/description_before.png" alt="Before" width="400"/>           | <img src="preview/pictures/description_after.png" alt="After" width="560"/>     |

**Legenda kolorów (typy wydarzeń):**

- ❤️ **Tomato** – Egzamin  
- 💜 **Grape** – Online lub Odwołane  
- 🖤 **Graphite** – Wykład  
- 💚 **Basil** – Ćwiczenia / Seminaria  
- 💙 **Peacock** – Laboratoria  
- 💛 **Banana** – Inne / Nieznane  

> **Możesz edytować kolory w słowniku `COLORS` w kodzie źródłowym.**

## 🛠️ Instalacja

1. **Wymagania:** Python 3.x
2. **Instalacja zależności:**

```bash
pip install gcsa ics pytz
```

## 🔑 Konfiguracja Google API

Aby skrypt mógł używać Kalendarza Google, wykonaj następujące kroki:

1. **Utwórz projekt GCP:** [Instrukcja](https://developers.google.com/workspace/guides/create-project)
   - Włącz **Google Calendar API**
2. **Skonfiguruj ekran zgody OAuth:** [Instrukcja](https://developers.google.com/workspace/guides/configure-oauth-consent)
3. **Utwórz dane logowania OAuth:** [Instrukcja](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id)
4. **Umieść plik `credentials.json` w katalogu `~/.credentials/`**

> Pomocna może być [szybka konfiguracja](https://developers.google.com/workspace/calendar/api/quickstart/python)

## 🎉 Użycie

### 🗓️ Przykład 1: Import do konkretnego kalendarza

```python
from main import ics_import
from config import calendar_id

ics_import(calendar_id)
```

### 🌐 Przykład 2: Utwórz nowy kalendarz i zaimportuj

```python
from main import ics_import

ics_import()
```

### 🕰️ Przykład 3: Edytuj plik ICS (zmiana strefy czasowej)

```python
from main import ics_edit

ics_edit()
```

## ⚙️ Jak to działa?

- **Obsługa kalendarza:** Tworzy nowy lub używa istniejącego.
- **Strefy czasowe:** Dopasowuje wydarzenia do Twojej strefy.
- **Sprzątanie:** Usuwa stare wydarzenia.
- **Kolory:** Przypisuje kolory wg typu wydarzenia.

## 🎨 Dostosowanie

- **Ścieżka do ICS:** Zmień `ics_path` w kodzie.
- **Logowanie:** Ustaw `open_browser=False`, jeśli już się autoryzowałeś.

## 🤝 Współpraca

**Masz pomysł lub poprawkę? Forkuj repozytorium, utwórz branch i wyślij pull requesta. Razem zrobimy to lepiej! 💪**

## 📜 Licencja

Na licencji [GNU General Public License v3](https://www.google.com/search?q=LICENSE)

## 📚 Dokumentacja

**Zajrzyj do dokumentacji biblioteki `gcsa`: [gcsa docs](https://google-calendar-simple-api.readthedocs.io/en/latest/index.html)**