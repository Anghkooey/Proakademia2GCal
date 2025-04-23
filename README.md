# ICS to Google Calendar Importer: Automated Import of ICS Schedules 📅✨

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
  <a href="docs/pl.md"><img src="docs/flags/pl_icon.svg" width="70" alt="Polish"></a>
  <a>  </a>
  <a href="README.md"><img src="docs/flags/en_icon.svg" width="70" alt="English"></a>
  <a>  </a>
  <a href="docs/ua.md"><img src="docs/flags/ua_icon.svg" width="70" alt="Ukrainian"></a>
</p>

**No more copying classes by hand! 😩 This Python script takes your **ICS (iCalendar)** file and automatically imports it into your **Google Calendar** — fast, clean, and smart. ✨**

**Originally built for [Uniwersytet Andrzeja Frycza Modrzewskiego](https://uafm.edu.pl/). You can get the ICS file from [this link](https://dziekanat.uafm.edu.pl/Plany/PlanyGrup)**.

**✔️ Auto-creates a calendar if you don’t have one  
✔️ Deletes old entries (older than 30 days)  
✔️ Cleans up and formats your schedule like a pro**

## ✨ Key Features

- **Effortless Import:** Automatically add your schedule to Google Calendar.
- **Universal Compatibility:** Works with ICS files from various university systems (e.g., APR System, Mobilny Student).
- **New Calendar Option:** Creates a new "Study" calendar if you don't specify one.
- **Clean Calendar:** Removes events older than 30 days before importing.
- **Color-Coded Events:** Visually distinguish event types (Exams ❤️, Lectures 🖤, etc.).
- **Time Zone Handling:** Uses your Google Calendar's time zone for accurate event times.

## 🚀 Quick Preview

See the magic happen! ✨ This animation shows how the script imports your ICS schedule into Google Calendar.

<div align="center">
<img src="docs/preview/preview.gif" alt="ICS to Google Calendar Import Preview" width="600">
</div>

<div align="center">
<h3>🗓️ Calendar View</h3>
</div>

|                      **Before**                      |                     **After**                      |
| :--------------------------------------------------: | :------------------------------------------------: |
| ![Before](docs/preview/pictures/calendar_before.png) | ![After](docs/preview/pictures/calendar_after.png) |

<div align="center">
  <h3><strong>📝 Event Description View</strong></h3>
</div>

|                                     **Before**                                     |                                    **After**                                     |
| :--------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| <img src="docs/preview/pictures/description_before.png" alt="Before" width="400"/> | <img src="docs/preview/pictures/description_after.png" alt="After" width="560"/> |

**Color legend (event types):**

- ❤️ **Tomato** – Exam
- 💜 **Grape** – Online or Cancelled
- 🖤 **Graphite** – Lecture
- 💚 **Basil** – Class / Seminar
- 💙 **Peacock** – Laboratory
- 💛 **Banana** – Other / Unknown

**You can change colors by editing the `COLORS` dictionary and related conditions in the code.**

## **Installation** 🛠️

1. **Prerequisites:** Make sure you have Python 3.x installed.
2. **Install Dependencies:**

```bash
pip install gcsa ics pytz
```

## 🔑 Setup Google API Credentials

Follow these steps to authorize the script to access your Google Calendar:

1. **Create a Google Cloud Platform (GCP) project:** [Guide](https://developers.google.com/workspace/guides/create-project)
   - **Important:** Enable the **Google Calendar API** for your project.
2. **Configure the OAuth consent screen:** [Guide](https://developers.google.com/workspace/guides/configure-oauth-consent)
3. **Create an OAuth client ID credential:** [Guide](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id) and download `credentials.json`.
4. **Store the credentials:** Place the downloaded `credentials.json` file in the `~/.credentials/` directory.

> **Note:** This [quickstart guide](https://developers.google.com/workspace/calendar/api/quickstart/python) might be helpful.

## 🎉 Usage

### 🗓️ Example 1: Import to a Specific Calendar

```python
from main import ics_import
from config import calendar_id

ics_import(calendar_id)
```

(Assuming you have `calendar_id` defined in `config.py`)

### 🌐 Example 2: Create a New Calendar and Import

```python
from main import ics_import

ics_import()
```

### 🕰️ Example 3: Edit ICS File (Adjust Time Zone)

```python
from main import ics_edit

ics_edit()
```

This function helps clean up and adjust event times.

## ⚙️ How It Works

- **Calendar Handling:** Creates a new "Study" calendar or uses an existing one.
- **Time Zone Magic:** Ensures events are in your calendar's time zone.
- **Cleanup Crew:** Removes old events to keep your calendar tidy.
- **Color Coordination:** Assigns colors based on event type.

## 🎨 Customization

- **ICS File Path:** Modify `ics_path` to use a different ICS file.
- **Authentication:** Set `open_browser=False` if you've already authenticated.

## 🤝 Contributing

**Feel free to contribute! Fork the repository, create a branch, and submit a pull request. Let's make this script even better together! 💪**

## 📜 License

**Licensed under the [GNU General Public License v3](https://www.google.com/search?q=LICENSE).**

## 📚 Documentation

**For detailed information about the `gcsa` library, visit: [gcsa Documentation](https://google-calendar-simple-api.readthedocs.io/en/latest/index.html)**
