from texpenses.models import TravelInfo, SecretaryPetitionSubmission


def create(self, validated_data):
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
    travel_info = validated_data.pop('travel_info', [])
    current_travel_info = instance.travel_info.all()
    for k, v in validated_data.iteritems():
        setattr(instance, k, v)
    instance.save()
    for i, travel in enumerate(travel_info):
        if i < len(current_travel_info) and current_travel_info:
            current_travel_obj = current_travel_info[i]
            for k, v in travel.iteritems():
                setattr(current_travel_obj, k, v)
            current_travel_obj.save()
        else:
            travel_obj = TravelInfo(travel_petition=instance, **travel)
            instance.travel_info.create(travel_petition=instance, **travel)
            travel_obj.save()
    return instance


def validate(self, attrs):
    attrs = super(self.__class__, self).validate(attrs)
    if 'user' not in attrs:
        attrs['user'] = self.context['request'].user
    model = self.Meta.model
    nested_attrs = attrs.pop('travel_info', [])
    for nested in nested_attrs:
        nested_inst = TravelInfo(travel_petition=model(**attrs), **nested)
        nested_inst.clean()
    model_inst = model(**attrs)
    model_inst.clean()
    attrs['travel_info'] = nested_attrs
    return attrs
