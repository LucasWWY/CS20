import json

from datetime import datetime, timedelta
from django.utils import timezone

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models.functions import Trunc

from project.models import Project, ProjectMember
from chat.models import ChatMassage, UserLastRoom


def history_msg(msg_time, talker, last_time_user, keyword=None, msg_type: int = False):
    send_data = {'history_msg': []}
    keyword = "" if keyword is None else keyword

    if msg_type:
        massage_list = ChatMassage.objects.filter(
            msg_type=2,
            talker=talker
        )
    else:
        if msg_time is None:
            massage_list = ChatMassage.objects.filter(
                content__icontains=keyword,
                talker=talker
            )
        else:
            zero_today = msg_time - timedelta(hours=msg_time.hour, minutes=msg_time.minute, seconds=msg_time.second,
                                              microseconds=msg_time.microsecond)
            last_today = zero_today + timedelta(hours=23, minutes=59, seconds=59)

            massage_list = ChatMassage.objects.filter(
                create_time__gte=zero_today,
                create_time__lte=last_today,
                content__icontains=keyword,
                talker=talker
            )

    for x in massage_list.all():
        msg = {'id': x.id,
               'sender': x.sender.id,
               'content': x.content,
               'name': str(x.sender),
               'create_time': x.create_time.strftime('%Y-%m-%d %H:%M:%S'),
               'msg_type': x.msg_type,
               'quote': x.quote.content if x.quote else None,
               'read': [],
               'unread': []}
        for last_time in last_time_user:
            if last_time.user != x.sender:
                if last_time.last_time > x.create_time:
                    msg['read'].append(str(last_time.user))
                else:
                    msg['unread'].append(str(last_time.user))
        send_data['history_msg'].append(msg)
    send_data['msg_date'] = [(x['date'] + timedelta(
        days=1)).timestamp() for x in massage_list.annotate(
        date=Trunc('create_time', 'day')).values('date').distinct()]
    return send_data


def update_last_time(user, project):
    UserLastRoom.objects.update_or_create({}, user=user, talker=project)


def create_massage(content, sender, talker, msg_type, quote=None):
    return ChatMassage.objects.create(content=content, sender=sender, talker=talker, msg_type=msg_type, quote=quote)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.project = Project.objects.filter(id=self.room_name).first()
        self.user_ide = Project.objects.filter(members__user=self.scope['user'], id=self.room_name).all()
        self.user_of_project = ProjectMember.objects.filter(project_id=self.room_name).all()
        self.last_time_user = UserLastRoom.objects.filter(talker=self.project)

        if self.user_ide:
            update_last_time(self.scope['user'], self.project)
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
        self.accept()
        if self.user_ide:
            send_data = history_msg(timezone.now(), self.project, self.last_time_user)
            send_data['users_list'] = [{"id": x.user.id, "name": str(x.user)} for x in
                                       ProjectMember.objects.filter(project_id=1).all()]
            self.send(json.dumps(send_data))

    def disconnect(self, close_code):
        if self.project:
            update_last_time(self.scope['user'], self.project)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        if self.user_ide:
            if message:
                if 'delete' in message:
                    ChatMassage.objects.filter(id=message['delete']).delete()
                elif 'search' in message:
                    gte_time = datetime.fromtimestamp(message['search']['gte']) if message['search'].get('gte') else None
                    if 'file' in message['search']:
                        send_data = history_msg(gte_time, self.project, self.last_time_user,
                                                msg_type=message['search']['file'])
                    else:
                        send_data = history_msg(gte_time, self.project, self.last_time_user,
                                                message['search']['keyword'], )
                    self.send(json.dumps(send_data))
                else:
                    if message['msg_type'] == 4:
                        mag_obj = create_massage(content=message['content'], sender=self.scope['user'],
                                                 talker=self.project, msg_type=message['msg_type'],
                                                 quote=ChatMassage.objects.filter(id=message['quote']).first())
                        message['quote'] = ChatMassage.objects.filter(id=message['quote']).first().content
                    else:
                        mag_obj = create_massage(content=message['content'], sender=self.scope['user'],
                                                 talker=self.project, msg_type=message['msg_type'])
                    message['id'] = mag_obj.id
                    # Send message to room group
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {"type": "chat_message", "message": message}
                    )

    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
