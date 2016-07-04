import logging
from django.contrib.auth import get_user_model
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import viewsets, filters, status, mixins
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import IsOwnerOrAdmin
from rest_framework.response import Response
from django.db.models import Q
from texpenses.serializers.factories import modelserializer_factory
from texpenses.models import (Accomondation, AdvancedPetition,
                              AdditionalExpenses, Petition, Flight)
from helper_methods import get_queryset_on_group

logger = logging.getLogger(__name__)

User = get_user_model()


class AccomondationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Accomondation info to be viewed or edited \
        (Secretary permissions and above are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, Accomondation)

    serializer_class = modelserializer_factory(Accomondation)


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

    def destroy(self, request, pk=None):
        print "Deleting advanced petition with id:" + str(pk)
        advanced_petition = self.get_object()
        print "--Deleting related flight:" + str(advanced_petition.flight)
        advanced_petition.flight.delete()
        print "--Done"
        print "--Deleting related accomondation:"\
            + str(advanced_petition.accomondation)
        advanced_petition.accomondation.delete()
        print "--Done"
        advanced_petition.delete()
        print "Done"

        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows user Flights to be viewed (from the Traveller)\
        or edited (Secretary permissions and above are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, Flight)

    serializer_class = modelserializer_factory(Flight)


class AdditionalExpensesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Additional Expenses to be created, viewed or\
        edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, AdditionalExpenses)

    serializer_class = modelserializer_factory(AdditionalExpenses)

    def create(self, request):
        petition = str(request.data['petition'])
        petition_id = petition[petition.index('user_petition') + 14:-1]

        petition_object = Petition.objects.get(id=petition_id)
        request.data['user'] = petition_object.user
        return super(AdditionalExpensesViewSet, self).create(request)


class UserPetitionViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows user related petitions to be viewed or edited \
        (permissions are needed)"""

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,
                          DjangoModelPermissions,)

    filter_backends = (filters.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = (
        'taskStartDate', 'taskEndDate', 'depart_date', 'return_date', 'project',
        'creationDate', 'updateDate',
        'movementCategory', 'departurePoint', 'arrivalPoint',
        'transportation', 'surname', 'iban', 'taxRegNum', 'status')
    ordering_fields = ('taskStartDate', 'taskEndDate', 'project',
                       'movementCategory', 'departurePoint', 'arrivalPoint',
                       'transportation', 'surname', 'iban', 'taxRegNum',)
    search_fields = ('name', 'surname',)
    ordering = ('project',)

    def get_queryset(self):
        request_user = self.request.user
        user_groups = request_user.groups.all()

        if user_groups:
            user_group_name = user_groups[0].name

        if request_user.is_staff or user_group_name == "SECRETARY":
            return Petition.objects.filter(Q(status__gte=2) |
                                           Q(user=request_user))
        else:
            return Petition.objects.filter(user=request_user)

    serializer_class = modelserializer_factory(Petition)

    def destroy(self, request, pk=None):

        petition = self.get_object()
        pet_status = petition.status.id

        user_groups = request.user.groups.all()
        user_group_name = 'Unknown'
        if user_groups:
            user_group_name = user_groups[0].name

        petition_status_to_delete = [1, 10]

        if user_group_name in ['SECRETARY', 'Unknown']:
            petition_status_to_delete = [1, 2, 3, 10]

        if pet_status in petition_status_to_delete:
            print "Deleting petition with id:" + str(pk)

            advanced_petition = petition.advanced_info

            print "--Deleting related Advanced"\
                "Petition with id:" + str(advanced_petition.id)
            advanced_petition.delete()
            print "----Deleting related flight:" + str(advanced_petition.flight)
            advanced_petition.flight.delete()
            print "----Done"

            print "----Deleting related accomondation"\
                + str(advanced_petition.accomondation)
            advanced_petition.accomondation.delete()
            print "----Done"
            print "--Done"
            petition.delete()
            print "Done"

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': "You dont have the permittions to delete"
                         "the specific Petition"},
                        status=status.HTTP_403_FORBIDDEN)
