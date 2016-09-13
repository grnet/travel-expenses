EXPOSED_METHODS = ['proceed']


def proceed(self, instance):
    """
    Method for proceeding a petition to next status by extending it.

    :param instance: Current petition object.
    """
    status = self.validated_data.pop('status')
    for attr, value in self.validated_data.items():
        setattr(instance, attr, value)
    instance.proceed_next_status(status)
    return instance
