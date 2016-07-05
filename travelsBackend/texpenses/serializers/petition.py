from texpenses.models import Compensation, FeedingKind,\
    Flight, Accomondation, AdvancedPetition, Petition
from django.conf import settings as django_settings
import datetime


# Naming convention for method naming: (create|update|delete)_ModelName

def create_AdditionalExpenses(self, validated_data):
    request = self.context['request']
    petition = str(request.data['petition'])
    petition_id = petition[petition.index('user_petition') + 14:-1]

    petition_object = Petition.objects.get(id=petition_id)
    request.data['user'] = petition_object.user
    validated_data['user'] = request.data['user']
    model_name = getattr(self.Meta, 'model')
    return model_name.objects.create(**validated_data)


def create_Petition(self, validated_data):
    user_object = self.context['request'].user
    validated_data['user'] = user_object

    validated_data['trip_days_before'] = user_object.trip_days_left

    arrival_point = validated_data['arrivalPoint']
    user_category = user_object.category

    compensation_object = None

    if arrival_point and user_category:
        country_category_name = arrival_point.country.category.name
        compensation_object = Compensation.objects.get(
            name=user_category.name + country_category_name)

    print "Create an empty advanced petition"

    ac = Accomondation(user=user_object, hotel="Hotel", hotelPrice=0.0)
    ac.save()
    fl = Flight(user=user_object, flightName="Flight", flightPrice=0.0)
    fl.save()
    feeding_kind_1 = FeedingKind.objects.get(id=1)
    ap = AdvancedPetition(accomondation=ac, flight=fl,
                          user=user_object,
                          compensation=compensation_object,
                          feeding=feeding_kind_1)
    ap.save()
    print "Done"
    validated_data['advanced_info'] = ap

    now = datetime.datetime.now()
    validated_data['creationDate'] = now
    validated_data['updateDate'] = now

    model_name = getattr(self.Meta, 'model')
    return model_name.objects.create(**validated_data)


def update_Petition(self, instance, validated_data):

    user_object = instance.user
    arrival_point = validated_data['arrivalPoint']

    user_category = user_object.category

    compensation_object = None
    status = validated_data['status']

    if arrival_point and user_category:
        country_category_name = arrival_point.country.category.name
        compensation_object = Compensation.objects.get(
            name=user_category.name + country_category_name)

    instance.advanced_info.compensation = compensation_object
    instance.advanced_info.save()
    submission_statuses = [2, 4, 5, 6, 7, 8, 9]

    if status.id in submission_statuses:
        user_object.trip_days_left = instance.trip_days_after()
        user_object.save()

    days_left = user_object.trip_days_left
    days_left_default = django_settings.MAX_HOLIDAY_DAYS

    if status.id == 10 and days_left < days_left_default:
        user_object.trip_days_left = days_left + \
            instance.transport_days()
        user_object.save()
    now = datetime.datetime.now()
    validated_data['updateDate'] = now
    return super(self.__class__, self).update(instance, validated_data)
