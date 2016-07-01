from rest_framework import serializers

from texpenses.models import AdditionalExpenses, Compensation, FeedingKind,\
    Flight, Accomondation, AdvancedPetition, Petition
from django.conf import settings as django_settings
import datetime


class AdditionalExpensesSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.data['user']

        return AdditionalExpenses.objects.create(**validated_data)

    class Meta:
        model = AdditionalExpenses
        fields = ('id', 'name', 'cost', 'petition', 'url')
        read_only_fields = ('id', 'url')


class UserPetitionSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):

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

        return Petition.objects.create(**validated_data)

    def update(self, instance, validated_data):

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
        return super(UserPetitionSerializer, self).update(instance,
                                                          validated_data)

    class Meta:
        model = Petition
        fields = ('id', 'name', 'surname', 'iban', 'specialtyID', 'kind',
                  'taxRegNum', 'taxOffice',
                  'taskStartDate', 'taskEndDate', 'depart_date', 'return_date',
                  'creationDate', 'updateDate',
                  'project', 'reason', 'movementCategory',
                  'departurePoint', 'arrivalPoint', 'overnights_num',
                  'overnights_num_proposed',
                  'overnight_cost', 'max_overnight_cost', 'overnights_sum_cost',
                  'transport_days', 'transport_days_proposed',
                  'task_duration', 'same_day_return_task',
                  'compensation_level', 'compensation_days',
                  'compensation_days_proposed',
                  'additional_expenses_sum', 'additional_expenses_initial',
                  'additional_expenses_initial_description',
                  'max_compensation', 'compensation_final', 'total_cost',
                  'transportation', 'recTransport', 'recAccomondation',
                  'recCostParticipation', 'advanced_info',
                  'status', 'user_category', 'trip_days_before',
                  'trip_days_after', 'url')
        read_only_fields = (
            'id', 'url', 'creationDate', 'updateDate', 'advanced_info')
