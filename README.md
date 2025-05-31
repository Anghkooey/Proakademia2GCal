# **Proakademia2GCal**: Supercharge Your [**Proakademia**](https://www.dlauczelni.apr.pl/) Calendar 📅✨

<p align="center">
  <a href="https://github.com/Anghkooey/Proakademia2GCal/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="License Badge">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
  </a>
  <a href="https://github.com/Anghkooey/Proakademia2GCal/commits/main">
    <img src="https://img.shields.io/github/last-commit/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="Last Commit Badge">
  </a>
  <a href="https://github.com/Anghkooey/Proakademia2GCal/releases">
    <img src="https://img.shields.io/github/release/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="Latest Release Badge">
  </a>
</p>

<p align="center">
<img src="https://img.shields.io/badge/🌏%20Click%20a%20flag%20to%20switch%20language-darkblue?style=for-the-badge" alt="Language switch hint"><br>
  <a href="docs/pl.md"><img src="docs/flags/pl_icon.svg" width="80" alt="Polish"></a>
  <a>  </a>
  <a href="README.md"><img src="docs/flags/en_icon.svg" width="80" alt="English"></a>
  <a>  </a>
  <a href="docs/ua.md"><img src="docs/flags/ua_icon.svg" width="80" alt="Ukrainian"></a>
</p>

---

**🚀 Tired of slow apps and messy schedules? Meet Proakademia2GCal!**

Created by a **[first-year student at UAFM](https://uafm.edu.pl/)** 🎓, this tool imports your **[Proakademia](https://www.dlauczelni.apr.pl/)** schedule straight into **[Google Calendar 🗓️](https://calendar.google.com/)** — fast, simple, and color-coded!

Why choose **Google Calendar**?

- ⚡ **Instant access** from **any device** — open it right in your **web browser** or via the official **mobile app** on **iOS** and **Android**
- 🌍 **Cross-platform convenience** — no need for extra apps or downloads to check your schedule
- 🎨 **Vibrant color-coding** for events: lectures 🖤, labs 💙, exams ❤️ — so your calendar is always clear and organized

**Proakademia2GCal lets you:**

- 🧹 **Clean and optimize your ICS file** for a smooth, error-free import
- 🗓️ **Automatically create a dedicated "Study" calendar** for your classes
- 🧼 **Keep your calendar clutter-free** by removing old events automatically

**Get started:**

- 🐍 Use the flexible **Python script** for maximum control
- 🚀 Or download ready-to-run apps for **[Windows](https://github.com/Anghkooey/Proakademia2GCal/releases)** 💻 and **[Linux](https://github.com/Anghkooey/Proakademia2GCal/releases)** 🐧

**Simplify your study life — schedule smarter, not harder!**

## 🚀 Quick Preview

See the magic happen! ✨ This animation shows how the script imports your ICS schedule into Google Calendar.

![ICS to Google Calendar Import Preview](docs/preview/preview.gif)

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

### 💻 Quick Install & Run

Want it fast and easy? Use the compiled executables from [**Releases**](https://github.com/Anghkooey/Proakademia2GCal/releases)!

- **Windows:** Grab `ics_edit_windows.exe` and go!

![ICS Edit Windows Usage](docs/preview/ics_edit_windows.gif)

- **Linux:** Grab `ics_edit_linux` and go!

**Heads up!** For those sweet color-coded events like in the preview, you'll need the Python script and `ics_import` (see Examples above). The executables handle the core import, but Python unlocks the color magic ✨.

### 🗓️ ICS File Import Guide

This is a general guide on how to import an ICS file into Google Calendar.

![Manual ICS Import](docs/preview/manual_import.gif)

## 🛠️ Installation & First-Time Setup

Getting started is easy — just follow these steps to supercharge your schedule with a few commands! ⚡

### 1. 💾 Clone the Repository

First, grab the project from GitHub:

```bash
git clone https://github.com/Anghkooey/Proakademia2GCal
```

### 2. 📦 Install Required Libraries

Before launching the script, make sure you have all dependencies:

```bash
pip install gcsa ics pytz oauthlib httplib2
```

### 3. 🚪 Enter the Source Directory

All the Python magic happens inside the `src/` folder. Navigate there:

```bash
cd Proakademia2GCal/src
```

Your environment is now ready to sync your academic calendar like a pro! ✅

## 🔑 Setup Google API Credentials

This step allows the script to connect to your Google Calendar securely via OAuth2.0 🔐

### Follow These Steps:

1. 🎛️ **Create a Google Cloud Platform (GCP) Project:**
   👉 [Step-by-step guide](https://developers.google.com/workspace/guides/create-project)
   ☑️ Make sure to enable the **Google Calendar API** in your project.

2. 🧾 **Configure the OAuth Consent Screen:**
   📘 [Follow this guide](https://developers.google.com/workspace/guides/configure-oauth-consent)
   Let Google know who’s asking for access (you).

3. 🔑 **Create OAuth 2.0 Client ID Credentials:**
   🛠️ Use this [official guide](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id)
   Then, download the generated `credentials.json` file.

4. 🗂️ **Place Your Credentials Correctly:**
   Move or copy the `credentials.json` to the following directory in your home folder:

   ```bash
   ~/.credentials/credentials.json
   ```

   > 💡 If the `.credentials/` directory doesn't exist — just create it!

📚 Need a visual walkthrough?
Google provides a great [Python Quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python) that walks you through the steps.

## 🎉 Usage

### 🗓️ Example 1: Import to a Specific Calendar

```python
from main import ics_import

calendar_id = "YOUR_CALENDAR_ID"  # Replace with your actual Calendar ID
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

---

### <a target="_blank" href="https://icons8.com/icon/Xm1BwlEApHW6/google-calendar">Google Calendar</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
