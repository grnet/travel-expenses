import json
from django.conf import settings


def load_resources():
    with open(settings.RESOURCES_FILE) as json_file:
        return json.load(json_file)


def user_directory_path(instance, filename):

    arrival_point_id = 'unknown_arrival_id'
    year = 'unknon_year'
    month = 'unknown_month'
    user = 'uknown_user'

    if instance.travel_info.all():
        arrival_point_id = instance.travel_info.last().arrival_point.id
        depart_date = instance.travel_info.first().depart_date
        year = depart_date.year
        month = depart_date.month
        user = instance.user.username
    filename = filename.encode('utf8')

    str_repr = '{0}/{1}/{2}_{3}/{4}'.format(user,
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
    'A': (220.0, 80.0),
    'B': (160.0, 60.0)
}

TRANSPORTATION_MODE_MIN_DISTANCE = {
    "BIKE": 160.00,
    "CAR": 160.00,
    "TRAIN": 120.00,
    "BUS": 120.00,
    "SHIP":  37.04
}

# this is used in case of domestic travel
MEANS_OF_TRANSPORT_DISTANCE_FACTOR = {
    "CAR": 0.15,
    "BIKE": 0.05
}

CATEGORIES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
)

COMPENSATION_CATEGORIES = {
    ('A', 'A'): 100.0,
    ('A', 'B'): 80.0,
    ('A', 'C'): 60.0,
    ('A', 'D'): 40.0,
    ('B', 'A'): 80.0,
    ('B', 'B'): 60.0,
    ('B', 'C'): 50.0,
    ('B', 'D'): 40.0,
}


# The relative amount of compensation based on the meals.
COMPENSATION_PROPORTION = {
    'NON': 1,
    'BRKF': 1,
    'SEMI': 0.5,
    'FULL': 0.25,
}
