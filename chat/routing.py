# -*- coding: utf-8 -*-
"""
File Name：     routing
Description :
date：          2024/3/20 020
"""
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
