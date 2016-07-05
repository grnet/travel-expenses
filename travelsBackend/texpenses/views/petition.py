import logging
from django.contrib.auth import get_user_model
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import IsOwnerOrAdmin
from django.db.models import Q
from texpenses.serializers.factories import modelserializer_factory
from texpenses.models import (Accomondation, AdvancedPetition,
                              AdditionalExpenses, Petition, Flight)
from texpenses.models.services import get_queryset_on_group
logger = logging.getLogger(__name__)


User = get_user_model()


class AdvancedPetitionViewSet(LoggingMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet
                              ):

    """API endpoint that allows Advanced petition info to be viewed or edited \
        (Secretary permissions and above are needed). An Advanced Petition is\
        created during simple Petition creation.
        """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, AdvancedPetition)

    serializer_class = modelserializer_factory(AdvancedPetition)
