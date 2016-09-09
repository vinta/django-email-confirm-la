# coding: utf8

import uuid


def generate_random_token():
    token = uuid.uuid4().hex

    return token
