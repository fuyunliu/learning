# -*- coding: utf-8 -*-
"""

"""


from celery import Celery


app = Celery(__name__, broker='redis://localhost:6379/0')


class Config:
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


app.config_from_object(Config)


@app.task
def add(x, y):
    return x + y


@app.task
def sub(x, y):
    return x - y


@app.task
def mul(x, y):
    return x * y
