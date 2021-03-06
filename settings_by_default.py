import os

VK_BOT_TOKEN = ''
GROUP_ID = 111
PASSWORD = ''

CITIES = ('Reykjavik', 'Oslo', 'Stockholm', 'Copenhagen', 'Torshavn')
CITIES_WITHOUT_CONNECTION = {'Stockholm', 'Torshavn'}
EVERY_TEN_DAYS_CITIES = {'Reykjavik', 'Torshavn'}  # two cities with flights at days even 10
EVERY_FRIDAY_CITIES = {'Stockholm', 'Reykjavik'}  # two cities with flights at fridays

# Datetime format settings
DATE_FORMAT = '%d/%m/%Y'
TIME_FORMAT = '%H:%M'
DATE_TIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

# Ticket settings
TEST_TICKET_PATH = os.path.normpath('external_data/ticket/ticket_test.png')
TICKET_TEMPLATE_PATH = os.path.normpath('external_data/ticket/ticket_template.png')
FONT_PATH = os.path.normpath('external_data/fonts/Stolzl-Medium.ttf')
FONT_SIZE_CITIES, FONT_SIZE = 78, 51


commands = ('/ticket', '/help', '/cities', '/routes', '/restart')

INTENTS = [
    {
        'name': 'Order ticket',
        'tokens': ('заказ', 'купить', 'найти', 'полёт'),
        'scenario': 'Ordering',
        'answer': None
    },
    {
        'name': 'Greeting',
        'tokens': ('hi', 'hello', 'здравствуй', 'прив'),
        'scenario': 'Greeting',
        'answer': None
    }
]

DEFAULT_ANSWER = "Я могу помочь заказать билет. Введи /help для получения подробной информации или /ticket для заказа"

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password=PASSWORD,
    host='localhost',
    database='scandinavian_airlines_bot'
)
SCENARIOS = {
    'Greeting': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Добро пожаловать в scandinavian airlines bot, {name}! '
                        'Введи /ticket для заказа или /help для получения подробной информации',
                'failure_text': 'Я могу обрабатывать только текстовые сообщения',
                'handler': 'greeting',
                'next_step': None,
            },
        }
    },
    'Help': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Если хочешь узнать все обслуживаемые города, отправь команду /cities .'
                        'Выбери команду /routes чтобы узнать все возможные маршруты.',
                'failure_text': 'Выбери одну из команд!',
                'handler': 'help_handler',
                'next_step': None,
            },
        }
    },
    'Ordering': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введи город отправления:\n\n\nТы можешь отправить команду /restart для перезапуска заказа',
                'failure_text': ' '.join(['Город должен быть из списка: \n', '\n'.join(CITIES)]),
                'handler': 'departure',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введи город прибытия:',
                'failure_text': ' '.join(['Город должен быть один из списка:\n',
                                          '\n'.join(CITIES)]),
                'handler': 'routes',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Был выбран рейс между {departure_city} и {destination_city}.'
                        'Введи день отправления в формате: ' + f'{DATE_FORMAT}.',
                'failure_text': 'Нет рейсов между этими городами.',
                'handler': 'route_info',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Выбери день вылета: ',
                'failure_text': 'Некорректный формат или выбранный день уже прошёл! Попробуй снова',
                'handler': 'date_handler',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Был выбран день рейса {departure_date}. Выбери время вылета: ',
                'failure_text': 'Попробуй снова',
                'handler': 'departure_date_handler',
                'next_step': 'step5.1'
            },
            'step5.1': {
                'text': 'Был выбран рейс между {departure_city} и {destination_city}\n'
                        '{departure_date}, в {departure_time}. Номер рейса: {flight_number}.\n'
                        'Введи количество билетов от 1 до 5',
                'failure_text': 'Попробуй снова',
                'handler': 'departure_time_handler',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Твой заказ {count_of_tickets} {ticket}. Можешь оставить комментарий к заказу.',
                'failure_text': 'От 1 до 5 включительно!',
                'handler': 'count_handler',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Данные верны?',
                'failure_text': None,
                'handler': 'comment',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Введи номер телефона в формате: +X XXXXXXXXXX',
                'failure_text': 'Отправь /restart чтобы изменить данные начав сначала',
                'handler': 'data_correct',
                'next_step': 'step9'
            },
            'step9': {
                'text': 'Укажи своё имя, если {name} не твоё настоящее имя',
                'failure_text': 'Некорректный номер. Попробуй снова!',
                'handler': 'phone_handler',
                'next_step': 'step10'
            },
            'step10': {
                'text': 'Твой номер телефона {phone}. Заказ: {count_of_tickets} {ticket} '
                        'из {departure_city} в {destination_city} {departure_date} в {departure_time}. '
                        'Перезвоним позже.',
                'failure_text': None,
                'handler': 'name_handler',
                'image': 'generates_ticket_handler',
                'next_step': None
            }
        }
    }
}
