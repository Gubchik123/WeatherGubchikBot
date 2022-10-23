<a href="https://t.me/WeatherGubchikBot" target="_blank"><img title="WeatherGubchikBot" alt="Header image" src="./images/WeatherGubchikBot_header.png"></a>
_Bot for showing information about the weather in cities of Ukraine and Europe_

### Demo

Click **<a href="https://t.me/WeatherGubchikBot" target="_blank">here</a>** to open telegram WeatherGubchikBot

### Project python modules (requirements.txt)

<img alt="aiogram" src="https://img.shields.io/pypi/v/aiogram?label=aiogram"> <img alt="asyncio" src="https://img.shields.io/pypi/v/asyncio?label=asyncio"> <img alt="beautifulsoup4" src="https://img.shields.io/pypi/v/beautifulsoup4?label=beautifulsoup4"> <img alt="lxml" src="https://img.shields.io/pypi/v/lxml?label=lxml"> <img alt="langdetect" src="https://img.shields.io/pypi/v/langdetect?label=langdetect"> <img alt="schedule" src="https://img.shields.io/pypi/v/schedule?label=schedule"> <img alt="emoji" src="https://img.shields.io/pypi/v/emoji?label=emoji"> <img alt="fuzzywuzzy" src="https://img.shields.io/pypi/v/fuzzywuzzy?color=blue&label=fuzzywuzzy"> <img alt="fake-useragent" src="https://img.shields.io/pypi/v/fake-useragent?label=fake-useragent&color=blue"> <img alt="psycopg2" src="https://img.shields.io/pypi/v/psycopg2?label=psycopg2"> <img alt="pyTelegramBotAPI" src="https://img.shields.io/pypi/v/pyTelegramBotAPI?label=pyTelegramBotAPI"> <img alt="python-Levenshtein" src="https://img.shields.io/pypi/v/python-Levenshtein?label=python-Levenshtein&color=blue"> <img alt="requests" src="https://img.shields.io/pypi/v/requests?label=requests">

---

### Features

1. <details><summary>Emoji</summary>I use RegExp for getting emoji by weather description</details>
2. <details><summary>Daily mailing</summary>You can sign up for the mailing to receive daily weather information in the city of your choice (you can turn it off at any time)</details>
3. <details><summary>Storing in database</summary>If you sign up for the newsletter, information will store in PostgreSQL database</details>
4. <details><summary>Using fuzzy comparison</summary>You can type the title of the city and bot try to find it with using python fuzzywuzyy module for fuzzy comparison</details>

### Three languages (screenshots)

**UA** <br>
<img title="WeatherGubchikBot" alt="Header image" src="./images/uk.jpg"> <br>
**EN** <br>
<img title="WeatherGubchikBot" alt="Header image" src="./images/en.jpg"> <br>
**RU** <br>
<img title="WeatherGubchikBot" alt="Header image" src="./images/ru.jpg"> <br>

### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DB_URI`
`BOT_TOKEN`

### Run Locally

Clone the project

```
  git clone https://github.com/Gubchik123/WeatherGubchikBot.git
```

Go to the project directory

```
  cd WeatherGubchikBot
```

Install dependencies

```
  pip install -r requirements.txt
```

Start the server

```
  python bot/bot.py
```

> **Note:** Don't forget about environment variables

### My contacts

<p align="left">
<a href="https://stackoverflow.com/users/20199410" target="_blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/stack-overflow.svg" height="30" width="40" /></a>
<a href="https://instagram.com/nikitos.1746" target="_blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" height="30" width="40" /></a>
<a href="https://t.me/Gubchik123" target="_blank"><img align="center" src="./images/icons8-telegram-app-48.png" width="40" /></a>
</p>
