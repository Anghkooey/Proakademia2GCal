# **Proakademia2GCal**: Покращте свій календар [**Proakademia**](https://www.dlauczelni.apr.pl/) 📅✨

<p align="center">
  <a href="https://github.com/Anghkooey/Proakademia2GCal/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="Значок ліцензії">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Значок Python">
  </a>
  <a href="https://github.com/Anghkooey/Proakademia2GCal/commits/main">
    <img src="https://img.shields.io/github/last-commit/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="Значок останнього коміту">
  </a>
  <a href="https://github.com/Anghkooey/Proakademia2GCal/releases">
    <img src="https://img.shields.io/github/release/Anghkooey/Proakademia2GCal?style=for-the-badge" alt="Значок останнього випуску">
  </a>
</p>

<p align="center">
  <a href="pl.md"><img src="flags/pl_icon.svg" width="80" alt="Польська"></a>
  <a>  </a>
  <a href="../README.md"><img src="flags/en_icon.svg" width="80" alt="Англійська"></a>
  <a>  </a>
  <a href="ua.md"><img src="flags/ua_icon.svg" width="80" alt="Українська"></a>
</p>

**Втомилися від проблем з додаванням розкладу занять з [Uniwersytetu Andrzeja Frycza Modrzewskiego (UAFM)](<(https://uafm.edu.pl/)>) до Календаря Google?** 😩 Як студент _UAFM_, я створив **Proakademia2GCal**, щоб спростити _редагування_ та _імпорт_ вашого розкладу з [**Proakademia**](https://www.dlauczelni.apr.pl/) до [**Календаря Google 🗓️**](https://calendar.google.com/), з яскравим кольоровим кодуванням та покращеною організацією.

Цей інструмент спрощує роботу з даними вашого розкладу, які зазвичай експортуються у форматі **ICS** з модуля "Деканат" системи [**Proakademia**](https://www.dlauczelni.apr.pl/) (використовується [**UAFM**](https://uafm.edu.pl/) та іншими університетами на базі [**APR**](https://www.apr.pl/) 🚀). Студенти _UAFM_ можуть легко отримати свій файл ICS з **[Деканату](https://dziekanat.uafm.edu.pl/Plany/PlanyGrup)** 🔗.

**Proakademia2GCal дозволяє вам:**

- ✔️ **Підготувати та покращити ваш файл ICS** для точного імпорту: налаштувати часові пояси та очистити дані.

- ✔️ **Імпортувати ваш розклад у спеціальний календар "Навчання" в Календарі Google** 🧙‍♂️ (з можливістю автоматичного створення).

- ✔️ **Підтримувати чистий календар** 🧼 завдяки автоматичному видаленню подій, старших за 30 днів.

- ✔️ **Інтуїтивно візуалізувати свій розклад** 🎨 з чітким форматуванням та _кольоровим кодуванням типів занять_ (наприклад, лекції 🖤, лабораторні 💙, іспити ❤️).

**Виберіть спосіб імпорту:**

- **Розробникам:** Використовуйте безпосередньо **скрипт Python** 🐍 для повного контролю.
- **Усім користувачам:** Завантажте **готові до використання програми** 🚀 для [**Windows**](https://github.com/Anghkooey/Proakademia2GCal/releases) 💻 та [**Linux**](https://github.com/Anghkooey/Proakademia2GCal/releases) 🐧.

## 🚀 Швидкий перегляд

**Подивіться, як це працює! ✨ Ця анімація показує, як скрипт імпортує ваш розклад ICS до Google Календаря.**

![Попередній перегляд імпорту ICS до Календаря Google](preview/preview.gif)

<div align="center">
<h3>🗓️ Перегляд календаря</h3>
</div>

|                   **До**                    |                   **Після**                   |
| :-----------------------------------------: | :-------------------------------------------: |
| ![До](preview/pictures/calendar_before.png) | ![Після](preview/pictures/calendar_after.png) |

<div align="center">
  <h3><strong>📝 Перегляд опису подій</strong></h3>
</div>

|                                  **До**                                   |                                  **Після**                                  |
| :-----------------------------------------------------------------------: | :-------------------------------------------------------------------------: |
| <img src="preview/pictures/description_before.png" alt="До" width="400"/> | <img src="preview/pictures/description_after.png" alt="Після" width="560"/> |

**Кольорова легенда (типи подій):**

- ❤️ **Томат** – Екзамен
- 💜 **Виноград** – Онлайн або Скасовано
- 🖤 **Графіт** – Лекція
- 💚 **Базилік** – Заняття / Семінар
- 💙 **Павич** – Лабораторна
- 💛 **Банан** – Інше / Невідомо

**Ви можете змінити кольори, редагуючи словник `COLORS` та відповідні умови в коді.**

### 💻 Швидка установка та запуск

Хочете швидко та легко? Використовуйте скомпільовані виконувані файли з [**Релізи**](https://github.com/Anghkooey/Proakademia2GCal/releases)!

- **Windows:** Завантажте `ics_edit_windows.exe` і вперед!

![Використання ICS Edit Windows](preview/ics_edit_windows.gif)

- **Linux:** Завантажте `ics_edit_linux` і вперед!

**Увага!** Для тих крутих кольорово-кодованих подій, як у попередньому перегляді, вам знадобиться скрипт Python та `ics_import` (дивіться Приклади вище). Виконувані файли обробляють основний імпорт, але Python відкриває кольорову магію ✨.

### 🗓️ Посібник з імпорту файлу ICS

Це загальний посібник про те, як імпортувати файл ICS у Календар Google.

![Ручний імпорт ICS](preview/manual_import.gif)

## 🛠️ Встановлення та Перший Запуск

Почати дуже просто — виконай ці кроки, щоб за лічені команди перетворити свій розклад у справжній Google Календар! ⚡

### 1. 💾 Клонування Репозиторію

Спочатку забери проєкт з GitHub:

```bash
git clone https://github.com/Anghkooey/Proakademia2GCal
```

### 2. 📦 Встановлення Необхідних Бібліотек

Перед запуском скрипта переконайся, що всі залежності встановлені:

```bash
pip install gcsa ics pytz oauthlib httplib2
```

### 3. 🚪 Перехід до Каталогу з Кодом

Уся фокусна логіка знаходиться в папці `src`. Перейди туди:

```bash
cd Proakademia2GCal/src
```

Твоє середовище готове — тепер можна професійно синхронізувати академічний календар! ✅

---

## 🔑 Налаштування Доступу до Google API

Цей крок дозволяє скрипту безпечно підключитися до твого Google Календаря через OAuth2.0 🔐

### Виконай ці дії:

1. 🎛️ **Створи проєкт у Google Cloud Platform (GCP):**
   👉 [Покрокова інструкція](https://developers.google.com/workspace/guides/create-project)
   ☑️ Обов’язково увімкни **Google Calendar API** для свого проєкту.

2. 🧾 **Налаштуй екран згоди OAuth:**
   📘 [Дотримуйся цього гайду](https://developers.google.com/workspace/guides/configure-oauth-consent)
   Щоб Google зрозумів, хто запитує доступ (тобто ти).

3. 🔑 **Створи облікові дані OAuth 2.0 (Client ID):**
   🛠️ Використай цей [офіційний посібник](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id)
   І завантаж отриманий файл `credentials.json`.

4. 🗂️ **Розмісти файл облікових даних належним чином:**
   Перенеси або скопіюй `credentials.json` у цю папку в домашньому каталозі:

   ```bash
   ~/.credentials/credentials.json
   ```

   > 💡 Якщо папки `.credentials/` не існує — просто створи її!

📚 Потрібен візуальний гайд?
Переглянь офіційний [Python Quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python) для детального покрокового опису.

## 🎉 Використання

### 🗓️ Приклад 1: Імпорт до конкретного календаря

```python
from main import ics_import

calendar_id = "YOUR_CALENDAR_ID"  # Замініть на фактичний ідентифікатор календаря
ics_import(calendar_id)
```

### 🌐 Приклад 2: Створити новий календар та імпортувати

```python
from main import ics_import

ics_import()
```

### 🕰️ Приклад 3: Редагувати ICS-файл (зміна часового поясу)

```python
from main import ics_edit

ics_edit()
```

Ця функція допомагає очистити і скоригувати час подій відповідно до вашого часового поясу.

## ⚙️ Як це працює

- **Робота з календарем:** Створює новий календар "Study" або використовує вже існуючий.
- **Часовий пояс:** Гарантує, що всі події відповідатимуть часовому поясу вашого календаря.
- **Очищення:** Видаляє старі події (старше 30 днів), щоб зберегти ваш календар охайним.
- **Кольори:** Призначає кольори подіям на основі їх типу.

## 🎨 Налаштування

- **Шлях до ICS:** Змініть змінну `ics_path`, щоб використовувати інший файл.
- **Автентифікація:** Встановіть `open_browser=False`, якщо ви вже авторизовані.

## 🤝 Співпраця

**Маєш ідеї? Бажаєш покращити скрипт? Форкай репозиторій, створи гілку та надсилай pull request. Зробимо цей інструмент ще кращим разом! 💪**

## 📜 Ліцензія

**Ліцензовано відповідно до [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.html).**

## 📚 Документація

**Офіційна документація для бібліотеки `gcsa`: [gcsa Documentation](https://google-calendar-simple-api.readthedocs.io/en/latest/index.html)**

---

### <a target="_blank" href="https://icons8.com/icon/Xm1BwlEApHW6/google-calendar">Google Calendar</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
