from django.core.exceptions import ValidationError
from texpenses.models import TravelInfo, SecretaryPetitionSubmission

EXPOSED_METHODS = [
    'create',
    'update',
    'validate',
]


def create(self, validated_data):
    """
    Method which overrides the `create` method of `HyperlinkedModelSerializer`
    class.

    This method sticks to the corresponding serializer classes of petition
    models and it actually implements the nested serialization for the
    creation of objects.

    There is an outlier case: When a `SecretaryPetitionSubmission` is created,
    then the available number user's trip days is updated accordingly, by
    removing the total transport days of trip.
    """
    travel_info = validated_data.pop('travel_info', [])
    petition = self.Meta.model.objects.create(**validated_data)
    for travel in travel_info:
        travel_obj = TravelInfo(travel_petition=petition, **travel)
        travel_obj.save()
        petition.travel_info.add(travel_obj)
        if self.Meta.model is SecretaryPetitionSubmission:
            petition.user.trip_days_left -= petition.transport_days()
            petition.user.save()
    return petition


def update(self, instance, validated_data):
    """
    Method which overrides the `update` method of `HyperlinkedModelSerializer`
    class.

    This method sticks to the corresponding serializer classes of petition
    models and it actually implements the nested serializationf for the
    update of objects.
    """
    travel_info = validated_data.pop('travel_info', [])
    validated_data.pop('dse', None)
    for k, v in validated_data.iteritems():
        setattr(instance, k, v)
    instance.save()
    _update_nested_objects(instance, travel_info)
    return instance


def _update_nested_objects(instance, nested_objects):
    """
    This function updates the nested model intances.

    There are three cases which describe how update of nested objects works.
    - If data include nested objects that already exist, then this method just
    updates them.
    - If data include nested objects that don't already exists (for example,
    add a new destination to an existing petition), then corresponding
    nested object is created.
    - If data include less nested objects than the currenly which are stored,
    then redundant model instances are deleted.
    """
    model_instances = instance.travel_info.all()
    for i, travel in enumerate(nested_objects):
        if i < len(model_instances) and model_instances:
            current_travel_obj = model_instances[i]
            for k, v in travel.iteritems():
                setattr(current_travel_obj, k, v)
            current_travel_obj.save()
        else:
            travel_obj = TravelInfo(travel_petition=instance, **travel)
            instance.travel_info.create(travel_petition=instance, **travel)
    for travel_obj in model_instances[len(nested_objects):]:
        travel_obj.delete()


def validate(self, attrs):
    """
    Method which overrides the `validate` method of
    `HyperlinkedModelSerializer` class.

    It validates both nested and main object.
    """
    if 'user' not in attrs:
        attrs['user'] = self.context['request'].user
    model = self.Meta.model
    nested_attrs = attrs.pop('travel_info', [])
    total_transport_days = 0
    for nested in nested_attrs:
        nested_inst = TravelInfo(travel_petition=model(**attrs), **nested)
        nested_inst.clean()
        total_transport_days += nested_inst.transport_days_manual\
            if nested_inst.transport_days_manual\
            else nested_inst.transport_days_proposed()
    model_inst = model(**attrs)
    validate_transport_days(attrs['user'], total_transport_days)
    model_inst.clean()
    attrs['travel_info'] = nested_attrs
    return attrs


def validate_transport_days(user, transport_days):
    """
    Check that total transport days don't surpass the number of user's
    available trip days.
    """
    if user.trip_days_left < transport_days:
        raise ValidationError(
            'You have exceeded the allowable number of trip days')
