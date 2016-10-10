import json
from django.conf import settings


def load_resources():
    with open(settings.RESOURCES_FILE) as json_file:
        return json.load(json_file)


def user_directory_path(instance, filename):
    travel_info = instance.travel_info.all()[0]
    arrival_point_id = travel_info.arrival_point.id
    depart_date = travel_info.depart_date
    year = depart_date.year
    month = depart_date.month
    filename = filename.encode('utf8')

    str_repr = '{0}/{1}/{2}_{3}/{4}'.format(instance.user.username,
                                            arrival_point_id, year,
                                            month, filename)
    return str_repr

RESOURCES = load_resources()
SPECIALTY = RESOURCES['SPECIALTY']
KIND = RESOURCES['KIND']
USER_CATEGORIES = RESOURCES['USER_CATEGORY']
MOVEMENT_CATEGORIES = RESOURCES['MOVEMENT_CATEGORIES']
TRANSPORTATION = RESOURCES['TRANSPORTATION']
MEALS = RESOURCES['MEALS']
WAYS_OF_PAYMENT = RESOURCES['WAYS_OF_PAYMENT']
CURRENCIES = RESOURCES['CURRENCIES']


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


# The relative amount of compensation based on the meals.
COMPENSATION_PROPORTION = {
    'NON': 1,
    'BRKF': 1,
    'SEMI': 0.5,
    'FULL': 0.25,
}
