### Getting started

This is a weather forecast project. Communication is done via a Telegram bot and all the forecasts made are in Moscow.

The pipeline is the following:
* The user opens Telegram client and starts a chat with the bot. All the interaction with the bot is done via buttons;
* The bot makes an API call to Yandex.Weather API;
* The bot creates a text response and sends it back to the client. The text response has the following format: 

<pre>
<b>Погода на YYYY-mm-dd:</b>
&ltweather&gt
Температура: &lttemperature&gt
Влажность: &lthumidity&gt
Давление: &ltpressure&gt
Скорость ветра: &ltwind_speed&gt
</pre>

The bot is hosted on Yandex Cloud Function and is written in Python. His name is LucasForecasterBot; feel free to chat with him.

### How to create another bot:
* Create the bot with Telegram's BotFather;
* Register in Yandex.Weather as a developer and fill your api token in bot's source code (located in start.py);
* Create a Yandex Cloud function (entry point: start.start);
* Upload the source code of the bot to the function;
* Set the bot's webhook to the endpoint of the function:
```
curl -F "url=https://functions.yandexcloud.net/<function_name>" "https://api.telegram.org/bot<bot_token>/setWebhook"
```
* Open a Telegram client, search the bot by name and choose 'START'.

You can watch an interaction with the bot in demo.mkv.
