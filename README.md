
### Admin Commands

```
/start - check bot alive or not 

/approve - Approve all join Requests
```

### Variables

* `API_HASH` Your API Hash from my.telegram.org
* `API_ID` Your API ID from my.telegram.org
* `BOT_TOKEN` Your bot token from @BotFather
* `SESSION_STRING` Pyrogram user session string. Get using [@TgSessionStringBot](https://telegram.dog/TgSessionStringBot)
* `OWNER_ID` Must enter Your Telegram Id
* `DATABASE_URI` Your Mongo DB URL
* `AUTH_CHANNEL` Your Channel ID eg:- -100xxxxxxxx
* `WELCOME_TEXT` Custom welcome message
   **Default:** `Hey {name}, your request to join {title} has been approved!`

### Fillings
#### WELCOME_TEXT
* `{name}` - User first name
* `{title}` - chat title

#### Deploy on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)</br>
