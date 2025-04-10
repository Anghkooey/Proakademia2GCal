# **ICS Importer for Google Calendar** 📅✨

<p align="center">
  <a href="pl.md"><img src="pl_icon.svg" width="70"></a>
  <a>&#8192;&#8192;</a>
  <a href="/README.md"><img src="en_icon.svg" width="70"></a>
  <a>&#8192;&#8192;</a>
  <a href="ua.md"><img src="ua_icon.svg" width="70"></a>
</p>

**Witamy w ICS Importer!** **Ten skrypt Pythona jest zaprojektowany do importowania wydarzeń z pliku** **ICS** **do Twojego** **Google Calendar**. **Jest on specjalnie dopasowany do importowania harmonogramów z** [**Uniwersytetu Andrzeja Frycza Modrzewskiego**](https://uafm.edu.pl/). **Plik ICS możesz pobrać** **[tutaj](https://dziekanat.uafm.edu.pl/Plany/PlanyGrup)**. **Jeśli nie masz jeszcze kalendarza, skrypt utworzy nowy. Dodatkowo, przed zaimportowaniem nowych wydarzeń, usunie stare (starsze niż 30 dni).**

![ICS Importer Screenshot](shot.png)

**Legenda kolorów (typy zajęć):**

- 🟥 **Tomato** – Egzamin  
- 🟪 **Grape** – Zajęcia online lub odwołane  
- ⬜ **Graphite** – Wykład  
- 🟩 **Basil** – Ćwiczenia / Seminarium  
- 🟦 **Peacock** – Laboratorium  
- 🟨 **Banana** – Inne / Nieznane  

**Możesz zmienić kolory, edytując słownik `COLORS` oraz odpowiadające warunki w kodzie.**

## **Instalacja** 🛠️

**Przed uruchomieniem skryptu upewnij się, że masz zainstalowane następujące zależności:**

```bash
pip install gcsa ics pytz
```

## **Konfiguracja Google API Credentials** 🔑

**Aby interagować z Twoim Google Calendar, musisz skonfigurować swoje dane uwierzytelniające API.**

### **Kroki, aby uzyskać dane uwierzytelniające Google API:**

1. **Utwórz nowy projekt w Google Cloud Platform (GCP)**  
   [Postępuj zgodnie z tym przewodnikiem, aby utworzyć projekt](https://developers.google.com/workspace/guides/create-project).  
   - **Ważne**: **Włącz** **Google Calendar API** **dla swojego projektu.**

2. **Skonfiguruj ekran zgody OAuth**  
   [Postępuj zgodnie z tym przewodnikiem, aby skonfigurować ekran zgody OAuth](https://developers.google.com/workspace/guides/configure-oauth-consent).

3. **Utwórz dane uwierzytelniające OAuth client ID**  
   [Utwórz dane uwierzytelniające OAuth i pobierz plik `credentials.json`](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id).

4. **Zapisz dane uwierzytelniające**  
   **Umieść pobrany plik** `credentials.json` **(client_secret_*.json) w katalogu** `~/.credentials/`.

> **Uwaga**: **Możesz znaleźć** [**ten przewodnik szybkiego startu**](https://developers.google.com/workspace/calendar/api/quickstart/python) **pomocnym przy konfiguracji danych uwierzytelniających API Google Calendar.**

## **Użycie** 🎉

### **Przykład 1: Importowanie wydarzeń do określonego kalendarza** 🗓️

**Jeśli masz już kalendarz:**

```python
from ics_import import ics_import
from config import calendar_id

ics_import(calendar_id)
```

### **Przykład 2: Utwórz nowy kalendarz i zaimportuj wydarzenia** 🌐

**Jeśli kalendarz nie jest podany, zostanie utworzony nowy:**

```python
from ics_import import ics_import

ics_import()
```

## **Jak to działa** ⚙️

- **Tworzenie lub używanie Google Calendar**: **Jeśli nie podano** `calendar_id`, **zostanie utworzony nowy kalendarz o nazwie "Study".**
- **Obsługa strefy czasowej**: **Skrypt używa strefy czasowej Twojego kalendarza dla godzin wydarzeń.**
- **Czyszczenie wydarzeń**: **Wydarzenia starsze niż 30 dni są usuwane przed dodaniem nowych.**
- **Kolorowanie wydarzeń**: **Wydarzeniom przypisane są kolory na podstawie ich typu** (np. **Egzamin**, **Online**, **Praca grupowa**).

## **Dostosowanie** 🎨

- **Ścieżka pliku ICS**: **Zmień parametr** `ics_path` **aby używać innego pliku ICS.**
- **Uwierzytelnianie**: **Pomiń uwierzytelnianie przeglądarką ustawiając** `open_browser=False` **jeśli już przeprowadziłeś uwierzytelnienie.**

## **Dokumentacja gcsa** 📚

**Pełną dokumentację biblioteki** `gcsa` **(która wchodzi w interakcję z API Google Calendar), znajdziesz tutaj:**  
[**Dokumentacja gcsa**](https://google-calendar-simple-api.readthedocs.io/en/latest/index.html)

## **Licencja** 📜

**Licencjonowane na warunkach GNU General Public License v3** - szczegóły znajdują się w pliku [**LICENSE**](/LICENSE).
