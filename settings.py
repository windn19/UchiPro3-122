token_telegram = 'your telegram token'

INTENTS = [
    {'name': 'Дата проведения',
     'tokens': ('когда', "сколько", "дата", "дату"),
     'scenario': None,
     'answer': 'Конференция проводится 15-го апреля, регистрация начнется в 10 утра'
     },
    {'name': 'Место проведения',
     'tokens': ('где', "место", "локация", "адрес", "метро"),
     'scenario': None,
     'answer': "Конференция пройдет в павильоне 18Г в Экспоцентре"
     },
    {'name': 'Регистрация',
     'tokens': ('регист', "добав"),
     'scenario': 'registration',
     'answer': None
     }
]

SCENARIOS = {
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Чтобы зарегистрироваться, введите ваше имя. Оно будет написано на бейджике',
                'failure_text': 'Имя должно состоять из 3-30 букв и дефиса. Попробуйте ещё раз',
                'handler': 'handler_name',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите email. Мы отправим на него все данные',
                'failure_text': 'Во введенном адресе ошибка. Попробуйте ещё раз',
                'handler': 'handler_email',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Спасибо за регистрацию, {name}! Мы отправили на {email} билет, распечатайте его',
                'failure_text': None,
                'handler': None,
                'next_step': None
            }
        }
    }
}

DEFAULT_ANSWER = 'Не знаю, как на это ответить. Могу сказать когда и где пройдет конференция,' \
                 ' а также зарегистрировать вас. Просто спросите'
