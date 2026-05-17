import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import random

TOKEN = "your_vk_token"
GROUP_ID = 1111111 #your VK group id

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

def menu():
    kb = VkKeyboard(inline=True)
    kb.add_callback_button('Список локаций', payload={'locations': '1'})
    kb.add_callback_button('Помощь', payload={'help': '1'})
    return kb

def locations():
    kb = VkKeyboard(inline=True)
    kb.add_callback_button('ФМШ', payload={'place': 'ФМШ'})
    kb.add_callback_button('Планета', payload={'place': 'Планета'})
    kb.add_line()
    kb.add_callback_button('◀ Назад', payload={'back': '1'})
    return kb

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        msg = event.object.message['text'].lower()
        peer = event.object.message['peer_id']

        if msg == "начать":
            vk.messages.send(
                peer_id=peer,
                message="👋 Привет! Я метеорологический бот.\n\nНажмите на кнопки ниже:",
                keyboard=menu().get_keyboard(),
                random_id=random.randint(1, 999999)
            )

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        peer = event.obj.peer_id
        payload = event.obj.payload

        try:
            vk.messages.sendMessageEventAnswer(
                event_id=event.obj.event_id,
                user_id=event.obj.user_id,
                peer_id=peer
            )
        except:
            pass

        if payload.get('locations') == '1':
            vk.messages.send(
                peer_id=peer,
                message="📍 Выберите локацию:",
                keyboard=locations().get_keyboard(),
                random_id=random.randint(1, 999999)
            )
        elif payload.get('help') == '1':
            vk.messages.send(
                peer_id=peer,
                message="📋 Помощь:\n• Нажмите 'Список локаций' для выбора интересующего вас места\n• Напишите 'начать' для главного меню\n• Если у вас остались вопросы, можете обратиться к создателю проекта: [piworearmpiwo|Владислав Биль]",
                random_id=random.randint(1, 999999)
            )
        elif payload.get('back') == '1':
            vk.messages.send(
                peer_id=peer,
                message="👋 Главное меню:",
                keyboard=menu().get_keyboard(),
                random_id=random.randint(1, 999999)
            )
        elif payload.get('place'):
            place = payload['place']
            weather_file = open(f'{place}','r',encoding='UTF-8')

            quantity = int(weather_file.readline())

            right_time = weather_file.readline()

            temperature_list = list(map(float, weather_file.readline().split()))
            temperature = round(sum(temperature_list) / quantity,2)

            humidity_list = list(map(float, weather_file.readline().split()))
            humidity = round(sum(humidity_list) / quantity,2)

            pressure_list = list(map(float, weather_file.readline().split()))
            pressure = round(sum(pressure_list) / quantity,2)
            carbon_dioxide_list = list(map(float, weather_file.readline().split()))
            carbon_dioxide = round(sum(carbon_dioxide_list) / quantity,2)



            vk.messages.send(
                peer_id=peer,
                message=f"🌡️Температура: {temperature} \n💧Влажность: {humidity} \n🗜Давление: {pressure} \n‍💨Углекислый газ: {carbon_dioxide} \n\n📍 Выберите локацию:",
                keyboard=locations().get_keyboard(),
                random_id=random.randint(1, 999999)
            )