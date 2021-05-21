import multiprocessing
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Count

from appSR.models import Numbers


class ChatConsumer(JsonWebsocketConsumer):
    groups = ['chat']
    users = []

    def connect(self):
        print('ACCEPT')
        self.accept()

    def receive_json(self, content):

        print('RECEIVE var: ', str(content['var']), str(self.users))
        user = str(content['user']) + "#" + str(content['hash'])

        if str(content['var']) == '0':
            tmp = 0
            for i in self.users:
                if i == str(content['user']) + "#" + str(content['hash']):
                    tmp += 1
            if tmp == 0:
                self.users.append(user)

        if str(content['var']) == '1':
            self.users.remove(user)
            print('EXIT: ', str(content['user']) + "#" + str(content['hash']))

        numbers = []
        tmp_chart_numbers = []
        tmp_chart_count = []
        chart_numbers = []
        chart_count = []
        numbers_bd = Numbers.objects.all()

        for elem in numbers_bd.all():
            numbers.append(elem.value)
            num_count = Numbers.objects.filter(value=elem.value).count()
            if not (elem.value in tmp_chart_numbers):
                tmp_chart_numbers.append(elem.value)
                tmp_chart_count.append(num_count)

        for i in range(1, 50):
            max_count = max(tmp_chart_count)
            chart_count.append(max_count)
            chart_numbers.append(tmp_chart_numbers[tmp_chart_count.index(max_count)])
            del tmp_chart_numbers[tmp_chart_count.index(max_count)]
            tmp_chart_count.remove(max_count)

        if str(content['var']) != '2':
            user = ""

        dt = datetime.now()

        async_to_sync(self.channel_layer.group_send)('chat', {
            'type': 'chat.message',
            'content': numbers,
            'users': self.users,
            'user': user,
            'chart_numbers': chart_numbers,
            'chart_count': chart_count,
            'datetime': dt.strftime("%d.%m.%Y, %H:%M:%S")
        })
        print('GET: ', str(content['user']) + "#" + str(content['hash']))

    def chat_message(self, message):
        # print('RECEIVE BROADCAST: ', message['users'])
        self.send_json({
            'content': message['content'],
            'users': message['users'],
            'chart_numbers': message['chart_numbers'],
            'chart_count': message['chart_count'],
            'user': message['user'],
            'datetime': message['datetime']
        })

    def disconnect(self, code):
        print('DISCONNECT')
