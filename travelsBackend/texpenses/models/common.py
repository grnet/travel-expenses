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


COMPENSATION_CATEGORIES = {
    ('A', 'A'): 220.0,
    ('A', 'C'): 220.0,
    ('A', 'B'): 220.0,
    ('B', 'A'): 220.0,
    ('B', 'B'): 220.0,
    ('B', 'C'): 220.0,
}
