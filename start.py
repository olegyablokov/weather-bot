import json
import requests

YANDEX_WEATHER_API_TOKEN = '<TOKEN>'

weather_condition_en_to_ru = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'partly-cloudy-and-light-rain': 'небольшой дождь',
    'partly-cloudy-and-rain': 'дождь',
    'overcast-and-rain': 'сильный дождь',
    'overcast-thunderstorms-with-rain': 'сильный дождь, гроза',
    'cloudy-and-light-rain': 'небольшой дождь',
    'overcast-and-light-rain': 'небольшой дождь',
    'cloudy-and-rain': 'дождь',
    'overcast-and-wet-snow': 'дождь со снегом',
    'partly-cloudy-and-light-snow': 'небольшой снег',
    'partly-cloudy-and-snow': 'снег',
    'overcast-and-snow': 'снегопад',
    'cloudy-and-light-snow': 'небольшой снег',
    'overcast-and-light-snow': 'небольшой снег',
    'cloudy-and-snow': 'снег'
}


def get_daily_forecast_text(weather, temperature, humidity, pressure,
                            wind_speed):
    return '{0}\nТемпература: {1}\nВлажность: {2}\nДавление: {3}\n' \
        'Скорость ветра: {4}'.format(
            weather_condition_en_to_ru[weather].capitalize(),
            '%.1f °C' % temperature,
            str(humidity) + '%',
            str(pressure) + ' мм рт.ст.',
            str(wind_speed) + ' м/с')


def get_forecast(forecast_type):
    endpoint = 'https://api.weather.yandex.ru/v1/forecast?' \
        'lat=55.7558&' \
        'lon=37.6173&' \
        'lang=ru_RU&' \
        'hours=false&' \
        'extra=false&' \
        'limit={0}'
    headers = {'X-Yandex-API-Key': YANDEX_WEATHER_API_TOKEN}

    def get_forecast_for_current_day(contents):
        return '<b>Прогноз на сегодня:</b>\n' + get_daily_forecast_text(
            contents['fact']['condition'],
            contents['fact']['temp'],
            contents['fact']['humidity'],
            contents['fact']['pressure_mm'],
            contents['fact']['wind_speed'])

    def get_forecast_for_future_days(forecasts):
        forecast = ''
        for daily_forecast in forecasts:
            day = daily_forecast['parts']['day']
            forecast += ('<b>Прогноз на {0}:</b>\n'.format(
                daily_forecast['date']) + get_daily_forecast_text(
                    day['condition'],
                    day['temp_avg'],
                    day['humidity'],
                    day['pressure_mm'],
                    day['wind_speed']
            )) + '\n\n'
        return forecast

    forecast = ''
    if forecast_type == 'current':
        contents = requests.get(endpoint.format(1), headers=headers).json()
        forecast = get_forecast_for_current_day(contents)
    elif forecast_type == 'tomorrow':
        contents = requests.get(endpoint.format(2), headers=headers).json()
        forecast = get_forecast_for_future_days(contents['forecasts'][1:2])
    elif forecast_type == '7_days':
        contents = requests.get(endpoint.format(7), headers=headers).json()
        forecast = get_forecast_for_current_day(contents) + '\n\n' + \
            get_forecast_for_future_days(contents['forecasts'][1:])
    else:
        raise('bad forecast_type')
    return forecast


def get_default_reply_markup():
    return {
        'keyboard': [[{'text': 'Прогноз на сегодня'},
                      {'text': 'Прогноз на завтра'},
                      {'text': 'Прогноз на 7 дней'}]]
    }


def start(event, context):
    body = json.loads(event['body'])
    input_text = body['message']['text']
    output_text = ''
    reply_markup = None

    try:
        if input_text == '/start':
            output_text = 'Привет! Я бот, который пишет прогноз погоды ' \
                'в Москве. Выбери интересующий тебя прогноз.'
            reply_markup = get_default_reply_markup()
        elif input_text == 'Прогноз на сегодня':
            output_text = get_forecast('current')
            reply_markup = {
                'keyboard': [[{'text': 'Запросить другой прогноз'}]]
            }
        elif input_text == 'Прогноз на завтра':
            output_text = get_forecast('tomorrow')
            reply_markup = {
                'keyboard': [[{'text': 'Запросить другой прогноз'}]]
            }
        elif input_text == 'Прогноз на 7 дней':
            output_text = get_forecast('7_days')
            reply_markup = {
                'keyboard': [[{'text': 'Запросить другой прогноз'}]]
            }
        elif input_text == 'Запросить другой прогноз':
            output_text = 'Какой прогноз тебя интересует?'
            reply_markup = get_default_reply_markup()
        else:
            output_text = 'Не понимаю тебя.'
            reply_markup = get_default_reply_markup()
    except BaseException:
        output_text = 'Извини, я сломан. Попробуй запросить прогноз позже.'

    answer = {
        'method': 'sendMessage',
        'chat_id': body['message']['chat']['id'],
        'text': output_text,
        'reply_markup': reply_markup,
        'parse_mode': 'html'
    }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': answer,
        'isBase64Encoded': False
    }
