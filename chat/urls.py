# -*- coding: utf-8 -*-
"""
File Name：     urls
Description :
date：          2024/3/20 020
"""

"""
docker run --name postgresql --privileged -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v /opt/docker_data/postgres/data:/var/lib/postgresql/data -d postgis/postgis:14-3.4
docker run -itd --name redis -p 6379:6379 redis:5
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]
