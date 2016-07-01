import logging
from django.contrib.auth import get_user_model
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import viewsets, filters, status, mixins
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from texpenses.custom_permissions import isAdminOrRead, IsOwnerOrAdmin
from rest_framework.response import Response
from django.db.models import Q

from texpenses.serializers import \
    AdditionalExpensesSerializer,\
    UserPetitionSerializer, modelserializer_factory
from texpenses.models import Project, MovementCategories, City, Country,\
    CountryCategory, Transportation, PetitionStatus, Accomondation,\
    AdvancedPetition, Flight, Compensation, AdditionalExpenses, Petition,\
    FeedingKind
from helper_methods import get_queryset_on_group, checkPetitionCompleteness,\
    checkAdvancedPetitionCompleteness, date_check
logger = logging.getLogger(__name__)

User = get_user_model()


class ProjectViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows project details to be viewed or edited\
        (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Project.objects.all()
    fields = ('id', 'name', 'accountingCode', 'url')
    serializer_class = modelserializer_factory(Project, fields)


class MovementCategoriesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows movement details to be viewed or edited\
         (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = MovementCategories.objects.all()
    fields = ('id', 'name', 'url')
    serializer_class = modelserializer_factory(MovementCategories, fields)


class CityViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows city info to be viewed or edited\
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = City.objects.all()
    fields = ('id', 'name', 'country', 'url')
    serializer_class = modelserializer_factory(City, fields)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['country']


class CountryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows country info to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Country.objects.all()
    fields = ('id', 'name', 'category', 'url')
    serializer_class = modelserializer_factory(Country, fields)


class CountryCategoryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows country categories to be viewed or edited\
         (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = CountryCategory.objects.all()
    fields = ('id', 'name', 'url')
    serializer_class = modelserializer_factory(CountryCategory, fields)


class TransportationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows transportation info to be viewed or edited\
        (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Transportation.objects.all()
    fields = ('id', 'name', 'url')
    serializer_class = modelserializer_factory(Transportation, fields)


class PetitionStatusViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = PetitionStatus.objects.all()
    fields = ('id', 'name', 'url')
    serializer_class = modelserializer_factory(PetitionStatus, fields)


class AccomondationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Accomondation info to be viewed or edited \
        (Secretary permissions and above are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, Accomondation)

    def update(self, request, pk=None):
        hotel = self.get_object()
        price = request.data['hotelPrice']

        hotel_cost = 0.0
        try:
            hotel_cost = float(price)
        except ValueError:
            hotel_cost = 0.0
            request.data['hotelPrice'] = hotel_cost

        max_overnight = 0

        advanced_petition = AdvancedPetition.objects.get(accomondation=hotel)

        petition = advanced_petition.petition

        if petition.user_category:
            max_overnight = petition.user_category.max_overnight_cost
        else:
            user = request.user
            max_overnight = user.category.max_overnight_cost

        if hotel_cost > max_overnight:
            return Response({'error': 'Hotel cost:' + str(hotel_cost) +
                             ' exceeds max hotel cost:' +
                             str(max_overnight)},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(AccomondationViewSet, self).update(request, pk)
    fields = ('id', 'hotel', 'hotelPrice', 'url')
    serializer_class = modelserializer_factory(Accomondation, fields)


class AdvancedPetitionViewSet(LoggingMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet
                              ):
    missing_field = None

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
    fields = ('id', 'petition', 'movement_num', 'dse', 'accomondation',
              'flight', 'feeding', 'non_grnet_quota', 'grnet_quota',
              'compensation', 'expenditure_protocol',
              'expenditure_date_protocol', 'movement_protocol',
              'movement_date_protocol', 'compensation_petition_protocol',
              'compensation_petition_date',
              'compensation_decision_protocol',
              'compensation_decision_date', 'url',
              'transport_days_manual', 'overnights_num_manual',
              'compensation_days_manual'
              )
    read_only_fields = ('id', 'url', 'petition')
    serializer_class = modelserializer_factory(
        AdvancedPetition, fields, read_only_fields)

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

    def update(self, request, pk=None):
        price = request.data['flightPrice']

        flight_cost = 0.0
        try:
            flight_cost = float(price)
        except ValueError:
            flight_cost = 0.0
            request.data['flightPrice'] = flight_cost

        return super(FlightViewSet, self).update(request, pk)
    fields = ('id', 'flightName', 'flightPrice', 'url')
    serializer_class = modelserializer_factory(Flight, fields)


class CompensationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows per country compensationw be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Compensation.objects.all()
    fields = ('id', 'name', 'country_category', 'user_category',
              'compensation', 'url')
    serializer_class = modelserializer_factory(Compensation, fields)


class AdditionalExpensesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Additional Expenses to be created, viewed or\
        edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        return get_queryset_on_group(request_user, AdditionalExpenses)

    serializer_class = AdditionalExpensesSerializer

    def create(self, request):
        petition = str(request.data['petition'])
        petition_id = petition[petition.index('user_petition') + 14:-1]

        petition_object = Petition.objects.get(id=petition_id)
        request.data['user'] = petition_object.user
        return super(AdditionalExpensesViewSet, self).create(request)


class FeedingViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Feeding info be created, viewed or edited \
        (Secretary permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = FeedingKind.objects.all()
    fields = ('id', 'name', 'url')
    serializer_class = modelserializer_factory(FeedingKind, fields)


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

    serializer_class = UserPetitionSerializer

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

    def create(self, request):
        request.data['user'] = request.user

        if request.data['status'] is None:
            return Response({'error': 'Missing petition status'},
                            status=status.HTTP_400_BAD_REQUEST)
        chosen_status = str(request.data['status'])

        chosen_status = chosen_status[
            chosen_status.index('status') + 7:-1]
        chosen_status = int(chosen_status)
        submission_statuses = [2, 4, 5, 6, 7, 8, 9]

        if chosen_status in submission_statuses:

            user_groups = request.user.groups.all()
            user_group_name = 'Unknown'
            if user_groups:
                user_group_name = user_groups[0].name

            is_petition_complete, missing_field = checkPetitionCompleteness(
                request, chosen_status)

            if is_petition_complete:
                tsd = request.data['taskStartDate']
                ted = request.data['taskEndDate']
                dd = None
                rd = None
                if chosen_status > 2:
                    dd = request.data['depart_date']
                    rd = request.data['return_date']
                date_check_result = date_check(tsd, ted, dd, rd,
                                               user_group_name,
                                               chosen_status)
                if date_check_result['error']:
                    return Response({'error': date_check_result['msg']},
                                    status=status.HTTP_400_BAD_REQUEST)

                if chosen_status == 4:
                    is_apetition_complete, ap_missing_field =\
                        checkAdvancedPetitionCompleteness(
                            self.get_object().advanced_info)
                    if is_apetition_complete is False:
                        return Response({'error': 'Advanced Petition is'
                                         'not complete,'
                                         'please insert all mandatory fields'
                                         '(missing field:' +
                                         ap_missing_field + ')'},
                                        status=status.HTTP_400_BAD_REQUEST)
                return super(UserPetitionViewSet, self).create(request)
            else:
                if missing_field is None:
                    return Response({'error': 'Petition is not complete,'
                                    ' please insert all mandatory fields'
                                    ' (missing field:' + "All"
                                    + ')'},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Petition is not complete,'
                                 ' please insert all mandatory fields'
                                 ' (missing field:' + str(missing_field)
                                 + ')'},
                                status=status.HTTP_400_BAD_REQUEST)

        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(UserPetitionViewSet, self).create(request)

    def update(self, request, pk=None):
        request.data['user'] = request.user

        if request.data['status'] is None:
            return Response({'error': 'Missing petition status'},
                            status=status.HTTP_400_BAD_REQUEST)

        chosen_status = str(request.data['status'])

        # import pdb
        # pdb.set_trace()
        chosen_status = chosen_status[
            chosen_status.index('status') + 7:-1]
        chosen_status = int(chosen_status)
        submission_statuses = [2, 4, 5, 6, 7, 8, 9]

        if chosen_status in submission_statuses:

            user_groups = request.user.groups.all()
            user_group_name = 'Unknown'
            if user_groups:
                user_group_name = user_groups[0].name

            is_petition_complete, missing_field = checkPetitionCompleteness(
                request, chosen_status)

            if is_petition_complete:
                tsd = request.data['taskStartDate']
                ted = request.data['taskEndDate']
                dd = None
                rd = None
                if chosen_status > 2:
                    dd = request.data['depart_date']
                    rd = request.data['return_date']
                date_check_result = date_check(tsd, ted, dd, rd,
                                               user_group_name,
                                               chosen_status)
                if date_check_result['error']:
                    return Response({'error': date_check_result['msg']},
                                    status=status.HTTP_400_BAD_REQUEST)
                if chosen_status == 4:
                    is_apetition_complete, ap_missing_field =\
                        checkAdvancedPetitionCompleteness(
                            self.get_object().advanced_info)
                    if is_apetition_complete is False:
                        return Response({'error': 'Advanced Petition is'
                                         ' not complete,'
                                         ' please insert all mandatory fields'
                                         ' (missing field:' +
                                         ap_missing_field + ')'},
                                        status=status.HTTP_400_BAD_REQUEST)

                return super(UserPetitionViewSet, self).update(request, pk)
            else:
                if missing_field is None:
                    return Response({'error': 'Petition is not complete,'
                                    ' please insert all mandatory fields'
                                    ' (missing field:' + "All"
                                    + ')'},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Petition is not complete,'
                                 ' please insert all mandatory fields'
                                 ' (missing field:' + missing_field + ')'},
                                status=status.HTTP_400_BAD_REQUEST)

        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(UserPetitionViewSet, self).update(request, pk)
