import json
from django.conf import settings


def load_resources():
    with open(settings.ENUM_FILE) as json_file:
        return json.load(json_file)


RESOURCES = load_resources()
SPECIALTY = RESOURCES['SPECIALTY']
KIND = RESOURCES['KIND']
USER_CATEGORIES = RESOURCES['USER_CATEGORY']
MOVEMENT_CATEGORIES = RESOURCES['MOVEMENT_CATEGORIES']
TRANSPORTATION = RESOURCES['TRANSPORTATION']
FEEDING = RESOURCES['FEEDING']
WAYS_OF_PAYMENT = RESOURCES['WAYS_OF_PAYMENT']


MAX_OVERNIGHT_COST = {
    'A': 220.0,
    'B': 160.0
}


COMPENSATION_CATEGORIES = {
    ('A', 'A'): 100.0,
    ('A', 'B'): 80.0,
    ('A', 'C'): 60.0,
    ('B', 'A'): 80.0,
    ('B', 'B'): 60.0,
    ('B', 'C'): 50.0,
}
