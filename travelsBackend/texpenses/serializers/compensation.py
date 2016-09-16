EXPOSED_METHODS = ['proceed']


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
