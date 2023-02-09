<a href="https://t.me/WeatherGubchikBot" target="_blank"><img title="WeatherGubchikBot" alt="Header image" src="./images/WeatherGubchikBot_header.png"></a>
_Bot for showing information about the weather in cities of Ukraine and Europe_

### Demo

Click **<a href="https://t.me/WeatherGubchikBot" target="_blank">here</a>** to open telegram WeatherGubchikBot

<img title="Demo" alt="Demo image" src="./images/demo.jpg">

### Project modules (requirements.txt)

<a href='https://pypi.org/project/aiogram'><img alt='aiogram' src='https://img.shields.io/pypi/v/aiogram?label=aiogram&color=blue'></a> <a href='https://pypi.org/project/asyncio'><img alt='asyncio' src='https://img.shields.io/pypi/v/asyncio?label=asyncio&color=blue'></a> <a href='https://pypi.org/project/APScheduler'><img alt='APScheduler' src='https://img.shields.io/pypi/v/APScheduler?label=APScheduler&color=blue'></a> <a href='https://pypi.org/project/beautifulsoup4'><img alt='beautifulsoup4' src='https://img.shields.io/pypi/v/beautifulsoup4?label=beautifulsoup4&color=blue'></a> <a href='https://pypi.org/project/lxml'><img alt='lxml' src='https://img.shields.io/pypi/v/lxml?label=lxml&color=blue'></a> <a href='https://pypi.org/project/emoji'><img alt='emoji' src='https://img.shields.io/pypi/v/emoji?label=emoji&color=blue'></a> <a href='https://pypi.org/project/fuzzywuzzy'><img alt='fuzzywuzzy' src='https://img.shields.io/pypi/v/fuzzywuzzy?label=fuzzywuzzy&color=blue'></a> <a href='https://pypi.org/project/fake-useragent'><img alt='fake-useragent' src='https://img.shields.io/pypi/v/fake-useragent?label=fake-useragent&color=blue'></a> <a href='https://pypi.org/project/psycopg2'><img alt='psycopg2' src='https://img.shields.io/pypi/v/psycopg2?label=psycopg2&color=blue'></a> <a href='https://pypi.org/project/python-dotenv'><img alt='python-dotenv' src='https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&color=blue'></a> <a href='https://pypi.org/project/python-Levenshtein'><img alt='python-Levenshtein' src='https://img.shields.io/pypi/v/python-Levenshtein?label=python-Levenshtein&color=blue'></a> <a href='https://pypi.org/project/pytz'><img alt='pytz' src='https://img.shields.io/pypi/v/pytz?label=pytz&color=blue'></a> <a href='https://pypi.org/project/requests'><img alt='requests' src='https://img.shields.io/pypi/v/requests?label=requests&color=blue'></a>

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
`TIMEZONE`
`BOT_TOKEN`
`MY_TELEGRAM_CHAT_ID`

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

Run the bot

```
  python bot/bot.py
```

> **Note:** Don't forget about environment variables
