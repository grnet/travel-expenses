def get_queryset_on_group(request_user, model):
    """TODO: Docstring for get_queryset_on_group.

    :user: TODO
    :returns: TODO

    """
    user_groups = request_user.groups.all()
    user_group_name = None

    if user_groups:
        user_group_name = user_groups[0].name

    if request_user.is_staff or user_group_name == "SECRETARY":

        return model.objects.all()
    else:
        return model.objects.filter(user=request_user)
