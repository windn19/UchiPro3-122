import re

import telebot

import handlers
from settings import token_telegram, INTENTS, DEFAULT_ANSWER, SCENARIOS

bot = telebot.TeleBot(token_telegram)
context = {}


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Это текстовый бот')


@bot.message_handler(content_types=['text'])
def answer_message(message: telebot.types.Message):
    id = message.chat.id
    text = message.text
    if id in context.keys():
        answer = continue_scen(text, id, context)
    else:
        for itens in INTENTS:
            if any(re.search(word, text.lower()) for word in itens['tokens']):
                if itens['scenario']:
                    answer = start_scen(itens['scenario'], id)
                    print(answer, context)
                else:
                    answer = itens['answer']
                break
        else:
             answer = DEFAULT_ANSWER
    # print(answer)
    bot.send_message(message.chat.id, answer)


def continue_scen(text, id, context):
    steps = SCENARIOS[context[id]['scen_name']]['steps']
    step = steps[context[id]['step_name']]
    handler = getattr(handlers, step['handler'])
    # print(handler)
    if handler(text, context[id]['context']):
        next_step = steps[step['next_step']]
        # print(next_step)
        answer = next_step['text'].format(**context[id]['context'])
        if next_step['next_step']:
            context[id]['step_name'] = step['next_step']
        else:
            # print(context)
            print('Регистрация {name} с адресом {email}'.format(**context[id]['context']))
            context.pop(id)
    else:
        answer = step['failure_text']
    return answer


def start_scen(scen, user_id):
    context[user_id] = {'scen_name': scen,
                        'step_name': SCENARIOS[scen]['first_step'],
                        'context': {}}
    return SCENARIOS[scen]['steps'][context[user_id]['step_name']]['text']


bot.infinity_polling()
