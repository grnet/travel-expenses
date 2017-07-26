from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied
from texpenses.models import Petition


class PetitionMixin(object):

    def create(self, validated_data):
        """
        Method which overrides the `create` method of
        `HyperlinkedModelSerializer`class.

        This method sticks to the corresponding serializer classes of petition
        models and it actually implements the nested serialization for the
        creation of objects.

        """
        # Check whether the petition of previous status is withdrawn, if yes
        # append the withdrawn field value to validated_data
        try:
            petition = Petition.objects.get(dse=validated_data['dse'],
                                            status=validated_data['status']-1,
                                            deleted=False)
            if petition.withdrawn:
                validated_data['withdrawn'] = True
        except Petition.DoesNotExist:
            pass

        validated_data.update({'status': 1})
        self.check_creation_allowed(validated_data)
        travel_info = validated_data.pop('travel_info', [])
        petition = self.Meta.model.objects.create(**validated_data)
        travel_info_model = self.fields['travel_info'].child.Meta.model

        for travel in travel_info:
            travel_obj = travel_info_model(travel_petition=petition, **travel)
            travel_obj.save(new_object=True)
            petition.travel_info.add(travel_obj)
        return petition

    def check_creation_allowed(self, data):
        """
        This functions checks that the petition can be created with the given
        dse value.

        Typically, when dse is not specified on request is automatically
        created by server. However, when dse is specified on request it must be
        associated with a petition created by the same user and there is not
        already a petition with the same dse but on greater status than the one
        defined on request.
        """
        dse = data.get('dse', None)
        if not dse:
            return

        relative_petition_filter = {'dse': dse, 'status__lt': data['status'],
                                    'user': data['user'], 'deleted': False,
                                    'task_start_date': data['task_start_date'],
                                    'task_end_date': data['task_end_date']}

        relative_petition_exclude_filter = {'dse': dse, 'user': data['user']}

        relative_records = Petition.objects.filter(**relative_petition_filter)

        dse_already_used = Petition.objects.\
            exclude(**relative_petition_exclude_filter).filter(dse=dse,
                                                               deleted=False)

        if dse_already_used.exists():
            raise PermissionDenied("A petition with dse:{0}, already exists."
                                   ", with data:{1}".
                                   format(dse, dse_already_used))

        if not relative_records.exists():
            raise PermissionDenied('Cannot create petition with dse %s' % (
                dse))

    def update(self, instance, validated_data):
        """
        Method which overrides the `update` method of
        `HyperlinkedModelSerializer` class.

        This method sticks to the corresponding serializer classes of petition
        models and it actually implements the nested serializationf for the
        update of objects.
        """

        travel_info = validated_data.pop('travel_info', [])
        for k, v in validated_data.iteritems():
            setattr(instance, k, v)

        instance.save()

        if travel_info:
            self._update_nested_objects(instance, travel_info)

        return instance

    def _update_nested_objects(self, instance, nested_objects):
        """
        This function updates the nested model intances.

        There are three cases which describe how update of nested objects
        works.
        - If data include nested objects that already exist, then this method
        just updates them.
        - If data include nested objects that don't already exists
        (for example, add a new destination to an existing petition),
        then corresponding nested object is created.
        - If data include less nested objects than the currenly which are
        stored, then redundant model instances are deleted.
        """
        request_user_group = self.context['request'].user.user_group()
        model_instances = instance.travel_info.all()
        for i, travel in enumerate(nested_objects):
            if i < len(model_instances) and model_instances:
                current_travel_obj = model_instances[i]
                for k, v in travel.iteritems():
                    setattr(current_travel_obj, k, v)

                if instance.status not in (
                    Petition.SAVED_BY_USER, Petition.SUBMITTED_BY_USER,
                    Petition.USER_COMPENSATION,
                    Petition.USER_COMPENSATION_SUBMISSION) and (
                        request_user_group != 'MANAGER'):
                        current_travel_obj._set_travel_manual_field_defaults()
                current_travel_obj.save()
            else:
                instance.travel_info.create(travel_petition=instance, **travel)
        for travel_obj in model_instances[len(nested_objects):]:
            travel_obj.delete()

    def validate(self, attrs):
        """
        Method which overrides the `validate` method of
        `HyperlinkedModelSerializer` class.

        It validates both nested and main object.
        """
        model = self.Meta.model
        nested_attrs = attrs.pop('travel_info', [])
        total_transport_days = 0
        travel_info_model = self.fields['travel_info'].child.Meta.model
        for nested in nested_attrs:
            nested_inst = travel_info_model(**nested)
            nested_inst.clean(model(**attrs))
            total_transport_days += nested_inst.transport_days_manual\
                if nested_inst.transport_days_manual\
                else nested_inst.transport_days_proposed()
        model_inst = model(**attrs)
        self.validate_transport_days(
            attrs.get('user', None), total_transport_days)
        model_inst.clean()

        attrs['travel_info'] = nested_attrs
        return attrs

    def proceed(self, instance):
        """
        Method for proceeding a petition to next status by extending it.

        :param instance: Current petition object.
        """
        kwargs = {}
        self.validated_data.pop('status')
        travel_info = self.validated_data.pop('travel_info', [])
        kwargs['petition_data'] = self.validated_data
        if travel_info:
            kwargs['travel_info_data'] = travel_info
        instance.proceed(**kwargs)
        return instance

    def validate_travel_info(self, value):
        travel_info_field = self.get_fields()['travel_info']
        if not travel_info_field.required:
            return value
        if not value or any(not obj for obj in value):
            raise ValidationError('This field must not include empty objects')
        return value

    def validate_user(self, user_value):
        user_field = self.get_fields()['user']
        if user_field.read_only:
            assert user_value is not None
            user_field.run_validators(user_value)
        return user_value

    def validate_transport_days(self, user, transport_days):
        """
        Check that total transport days don't surpass the number of user's
        available trip days.
        """
        if user and user.trip_days_left < transport_days:
            raise ValidationError(
                'You have exceeded the allowable number of trip days')
