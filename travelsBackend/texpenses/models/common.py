import json

DEFAULT_RESOURCE_LOCATION = "../resources/common.json"


def load_resources():
    with open(DEFAULT_RESOURCE_LOCATION) as json_file:
        return json.load(json_file)


RESOURCES = load_resources()
SPECIALTY = RESOURCES['SPECIALTY']
KIND = RESOURCES['KIND']
USER_CATEGORIES = RESOURCES['USER_CATEGORY']
MOVEMENT_CATEGORIES = RESOURCES['MOVEMENT_CATEGORIES']
TRANSPORTATION = RESOURCES['TRANSPORTATION']
FEEDING = RESOURCES['FEEDING']


COMPENSATION_CATEGORIES = {
    ('1', '1'): 220.0,
    ('1', '2'): 220.0,
    ('1', '3'): 220.0,
    ('2', '1'): 220.0,
    ('2', '2'): 220.0,
    ('2', '3'): 220.0,
}
