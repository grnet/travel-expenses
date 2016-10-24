from rest_framework import viewsets, mixins
from django.db import transaction


class UpdateModelMixinAtomic(mixins.UpdateModelMixin):

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super(UpdateModelMixinAtomic, self).\
            update(request, *args, **kwargs)


class DestroyModelMixinAtomic(mixins.DestroyModelMixin):

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(DestroyModelMixinAtomic, self).\
            destroy(request, *args, **kwargs)


class ModelViewSetAtomic(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         UpdateModelMixinAtomic,
                         DestroyModelMixinAtomic,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    pass
