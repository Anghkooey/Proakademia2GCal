# **ICS Importer для Google Calendar** 📅✨

<p align="center">
  <a href="pl.md"><img src="pl_icon.svg" width="70"></a>
  <a>&#8192;&#8192;</a>
  <a href="/README.md"><img src="en_icon.svg" width="70"></a>
  <a>&#8192;&#8192;</a>
  <a href="ua.md"><img src="ua_icon.svg" width="70"></a>
</p>

**Ласкаво просимо до ICS Importer!** **Цей Python-скрипт призначений для імпорту подій з файлу** **ICS** **у ваш** **Google Calendar**. **Він спеціально налаштований для імпорту розкладів з** [**Університету Анджея Фрича Моджевського**](https://uafm.edu.pl/). **Файл ICS можна отримати** **[тут](https://dziekanat.uafm.edu.pl/Plany/PlanyGrup)**. **Якщо у вас ще немає календаря, скрипт створить новий. Крім того, перед імпортом нових подій він видалить старі (старші за 30 днів).**

![ICS Importer Screenshot](shot.png)

**Легенда кольорів (типи занять):**

- 🟥 **Tomato** – Екзамен  
- 🟪 **Grape** – Онлайн або скасоване заняття  
- ⬜ **Graphite** – Лекція  
- 🟩 **Basil** – Семінар / Практика  
- 🟦 **Peacock** – Лабораторна робота  
- 🟨 **Banana** – Інше / Невідоме  

**Ви можете змінити кольори, відредагувавши словник `COLORS` та відповідні умови в коді.**

## **Інсталяція** 🛠️

**Перед запуском скрипта переконайтеся, що у вас встановлені наступні залежності:**

```bash
pip install gcsa ics pytz
```

## **Налаштування Google API Credentials** 🔑

**Щоб взаємодіяти з вашим Google Calendar, потрібно налаштувати ваші облікові дані API.**

### **Кроки для отримання облікових даних Google API:**

1. **Створіть новий проект у Google Cloud Platform (GCP)**  
   [Дотримуйтесь цього посібника для створення проекту](https://developers.google.com/workspace/guides/create-project).  
   - **Важливо**: **Увімкніть** **Google Calendar API** **для вашого проекту.**

2. **Налаштуйте екран згоди OAuth**  
   [Дотримуйтесь цього посібника для налаштування екрану згоди OAuth](https://developers.google.com/workspace/guides/configure-oauth-consent).

3. **Створіть облікові дані OAuth client ID**  
   [Створіть облікові дані OAuth і завантажте файл `credentials.json`](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id).

4. **Збережіть облікові дані**  
   **Помістіть завантажений файл** `credentials.json` **(client_secret_*.json) у каталог** `~/.credentials/`.

> **Примітка**: **Ви можете знайти** [**цей посібник для швидкого старту**](https://developers.google.com/workspace/calendar/api/quickstart/python) **корисним при налаштуванні облікових даних Google Calendar API.**

## **Використання** 🎉

### **Приклад 1: Імпортування подій до конкретного календаря** 🗓️

**Якщо у вас вже є календар:**

```python
from ics_import import ics_import
from config import calendar_id

ics_import(calendar_id)
```

### **Приклад 2: Створення нового календаря та імпорт подій** 🌐

**Якщо календар не вказано, буде створено новий:**

```python
from ics_import import ics_import

ics_import()
```

## **Як це працює** ⚙️

- **Створення або використання Google Calendar**: **Якщо не вказано** `calendar_id`, **створюється новий календар з назвою "Study".**
- **Обробка часових зон**: **Скрипт використовує часову зону вашого календаря для подій.**
- **Очищення подій**: **Події старші за 30 днів видаляються перед додаванням нових.**
- **Кодування кольорів**: **Подіям надаються кольори залежно від їх типу** (наприклад, **Екзамен**, **Онлайн**, **Групова робота**).

## **Налаштування** 🎨

- **Шлях до файлу ICS**: **Змініть параметр** `ics_path` **для використання іншого файлу ICS.**
- **Аутентифікація**: **Пропустіть аутентифікацію через браузер, встановивши** `open_browser=False`, **якщо ви вже виконали аутентифікацію.**

## **Документація gcsa** 📚

**Повну документацію бібліотеки** `gcsa` **(яка взаємодіє з Google Calendar API), можна знайти тут:**  
[**Документація gcsa**](https://google-calendar-simple-api.readthedocs.io/en/latest/index.html)

## **Ліцензія** 📜

**Ліцензовано за умовами GNU General Public License v3** - подробиці у файлі [**LICENSE**](/LICENSE).