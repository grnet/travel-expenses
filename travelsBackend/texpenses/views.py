import requests
import urllib
import logging
import datetime

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser import views as djoser_views
from django.conf import settings
from django.db.models import Q

from rest_framework import viewsets, filters, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication

from rest_framework_tracking.mixins import LoggingMixin
from models import Specialty
from models import TaxOffice
from models import Kind
from models import Petition
from models import Project
from models import MovementCategories
from models import City
from models import Country
from models import CountryCategory
from models import Transportation
from models import PetitionStatus
from models import UserCategory

from models import AdditionalExpenses
from models import Compensation
from models import FeedingKind
from models import Flight
from models import Accomondation
from models import AdvancedPetition


from serializers import UserProfileSerializer
from serializers import SpecialtySerializer
from serializers import TaxOfficeSerializer
from serializers import KindSerializer
from serializers import CustomUserRegistrationSerializer
from serializers import CitySerializer
from serializers import CountrySerializer
from serializers import CountryCategorySerializer
from serializers import MovementCategoriesSerializer
from serializers import ProjectSerializer
from serializers import TransportationSerializer
from serializers import UserPetitionSerializer
from serializers import PetitionStatusSerializer
from serializers import UserCategorySerializer

from serializers import AdditionalExpensesSerializer
from serializers import AdvancedPetitionSerializer
from serializers import FlightSerializer
from serializers import AccomondationSerializer
from serializers import FeedingKindSerializer
from serializers import CompensationSerializer

from custom_permissions import isAdminOrRead
from custom_permissions import IsOwnerOrAdmin
logger = logging.getLogger(__name__)

User = get_user_model()


@require_http_methods(["GET", ])
def custom_activation_view(request, uid=None, token=None):
    if uid and token:
        payload = {
            'uid': uid,
            'token': token
        }
        enc = urllib.urlencode(payload)
        url = settings.HOST_URL + 'auth/activate/'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=enc, headers=headers)
        if response.status_code == 200:
            return HttpResponse("ACTIVATED")
        elif response.status_code == 403:
            return HttpResponse("ALREADY ACTIVATED")
        else:
            return HttpResponse("Could not activate account with uid:" +
                                uid + " and token:" + token)


class CustomUserView(LoggingMixin, djoser_views.UserView):

    """API endpoint that lets a user view and edit some basic\
        user related info"""
    pass


class CustomActivationView(LoggingMixin, djoser_views.ActivationView):

    """API endpoint that activates a new user account"""
    pass


class CustomSetUsernameView(LoggingMixin, djoser_views.SetUsernameView):

    """API endpoint that lets a user change his/her username"""
    pass


class CustomSetPasswordView(LoggingMixin, djoser_views.SetPasswordView):

    """API endpoint that lets a user change his/her password"""
    pass


class CustomPasswordResetView(LoggingMixin, djoser_views.PasswordResetView):

    """API endpoint that sends email to user with password reset link"""
    pass


class CustomPasswordResetConfirmView(LoggingMixin,
                                     djoser_views.PasswordResetConfirmView):

    """Use this endpoint to finish reset password process"""
    pass


class CustomLoginView(LoggingMixin, djoser_views.LoginView):

    """Use this endpoint to obtain user authentication toke"""
    pass


class CustomLogoutView(LoggingMixin, djoser_views.LogoutView):

    """API endpoint for logging out a user"""
    pass


class CustomRootView(LoggingMixin, djoser_views.RootView):

    """API endpoint that lists all user related API endpoints"""
    pass


class CustomUserDetailedView(LoggingMixin, djoser_views.UserView):

    """API endpoint that allows a user to view and edit his personal info"""

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.all()


class SpecialtyViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user) """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class KindViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class TaxOfficeViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer


class UserCategoryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited\
        (by a permitted user)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer


class CustomUserRegistrationView(LoggingMixin, djoser_views.RegistrationView):

    """API endpoint for registering a new user"""
    serializer_class = CustomUserRegistrationSerializer


class ProjectViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows project details to be viewed or edited\
        (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MovementCategoriesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows movement details to be viewed or edited\
         (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = MovementCategories.objects.all()
    serializer_class = MovementCategoriesSerializer


class CityViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows city info to be viewed or edited\
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ['country']


class CountryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows country info to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryCategoryViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows country categories to be viewed or edited\
         (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = CountryCategory.objects.all()
    serializer_class = CountryCategorySerializer


class TransportationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows transportation info to be viewed or edited\
        (permissions are needed) """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer


class PetitionStatusViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = PetitionStatus.objects.all()
    serializer_class = PetitionStatusSerializer


class AccomondationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Accomondation info to be viewed or edited \
        (Secretary permissions and above are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user

        user_groups = request_user.groups.all()

        if user_groups:
            user_group_name = user_groups[0].name

        if request_user.is_staff or user_group_name == "SECRETARY":

            return Accomondation.objects.all()
        else:
            return Accomondation.objects.filter(user=request_user)

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

    serializer_class = AccomondationSerializer


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
        user_groups = request_user.groups.all()

        if user_groups:
            user_group_name = user_groups[0].name

        if request_user.is_staff or user_group_name == "SECRETARY":
            return AdvancedPetition.objects.all()
        else:
            return AdvancedPetition.objects.filter(user=request_user)
    serializer_class = AdvancedPetitionSerializer

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
        user_groups = request_user.groups.all()

        if user_groups:
            user_group_name = user_groups[0].name

        if request_user.is_staff or user_group_name == "SECRETARY":
            return Flight.objects.all()
        else:
            return Flight.objects.filter(user=request_user)

    def update(self, request, pk=None):
        price = request.data['flightPrice']

        flight_cost = 0.0
        try:
            flight_cost = float(price)
        except ValueError:
            flight_cost = 0.0
            request.data['flightPrice'] = flight_cost

        return super(FlightViewSet, self).update(request, pk)
    serializer_class = FlightSerializer


class CompensationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows per country compensationw be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Compensation.objects.all()
    serializer_class = CompensationSerializer


class AdditionalExpensesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows Additional Expenses to be created, viewed or\
        edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        user_groups = request_user.groups.all()

        if user_groups:
            user_group_name = user_groups[0].name

        if request_user.is_staff or user_group_name == "SECRETARY":
            return AdditionalExpenses.objects.all()
        else:
            return AdditionalExpenses.objects.filter(user=request_user)
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
    serializer_class = FeedingKindSerializer


class UserPetitionViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows user related petitions to be viewed or edited \
        (permissions are needed)"""
    missing_field = None

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
            # return Petition.objects.all()
        else:
            return Petition.objects.filter(user=request_user)

    serializer_class = UserPetitionSerializer

    def checkPetitionCompleteness(self, request, status):
        """TODO: Docstring for checkDataCompleteness.

        :request: TODO
        :returns: TODO

        """
        user_groups = request.user.groups.all()
        user_group_name = 'Unknown'
        if user_groups:
            user_group_name = user_groups[0].name
        try:
            name = request.data['name']
            surname = request.data['surname']
            iban = request.data['iban']
            specialtyID = request.data['specialtyID']
            taxRegNum = request.data['taxRegNum']
            taxOffice = request.data['taxOffice']
            kind = request.data['kind']
            taskStartDate = request.data['taskStartDate']
            taskEndDate = request.data['taskEndDate']
            if status > 2:
                depart_date = request.data['depart_date']
                return_date = request.data['return_date']
            project = request.data['project']
            reason = request.data['reason']
            movementCategory = request.data['movementCategory']
            departurePoint = request.data['departurePoint']
            arrivalPoint = request.data['arrivalPoint']
            transportation = request.data['transportation']
        except KeyError:
            print "Shit"

            return False

        none_mandatory_fields = ['accomondation', 'recCostParticipation',
                                 'recTransport', 'recAccomondation',
                                 'depart_date', 'return_date', 'advanced_info']
        if user_group_name in ['SECRETARY', 'Unknown']:
            none_mandatory_fields = ['accomondation', 'recCostParticipation',
                                     'recTransport', 'recAccomondation',
                                     'advanced_info']
        keys = request.data.keys()

        for key in keys:
            if key not in none_mandatory_fields:
                value = request.data[key]
                if value is None or value == '':
                    self.missing_field = key
                    return False
            else:
                continue

        return True

    def checkAdvancedPetitionCompleteness(self, advanced_petition):

        none_mandatory_fields = ['compensation_petition_protocol',
                                 'compensation_petition_date',
                                 'compensation_decision_protocol',
                                 'compensation_decision_date']

        for f in advanced_petition._meta.get_fields():
            field_name = f.name
            field_value = getattr(advanced_petition, f.name)
            print field_name + ":" + str(field_value)
            if field_value is None and field_name not in none_mandatory_fields:
                self.missing_field = f.name
                return False

        return True

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

    def date_check(self, task_start, task_end, depart_date, return_date,
                   user_group, status):

        result = {'error': False, 'msg': ''}
        now = datetime.datetime.now()

        task_start = datetime.datetime.strptime(
            task_start, '%Y-%m-%dT%H:%M')

        task_end = datetime.datetime.strptime(
            task_end, '%Y-%m-%dT%H:%M')

        if task_start < now:
            result['error'] = True
            result['msg'] = 'Task start date should be after today'
            return result

        if task_end < now:

            result['error'] = True
            result['msg'] = 'Task end date should be after today'
            return result

        if task_end < task_start:

            result['error'] = True
            result['msg'] = 'Task end date should be after task start date'
            return result

        if user_group in ['SECRETARY', 'Unknown'] and status > 2:
            depart_date = datetime.datetime.strptime(
                depart_date, '%Y-%m-%dT%H:%M')

            return_date = datetime.datetime.strptime(
                return_date, '%Y-%m-%dT%H:%M')
            if depart_date < now:
                result['error'] = True
                result['msg'] = 'Depart date should be after today'
                return result

            if return_date < now:
                result['error'] = True
                result['msg'] = 'Return date should be after today'
                return result

            if return_date < depart_date:

                result['error'] = True
                result['msg'] = 'Return date should be after departure date'
                return result
        return result

    def create(self, request):
        request.data['user'] = request.user

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

            print request.data

            if self.checkPetitionCompleteness(request, chosen_status):
                tsd = request.data['taskStartDate']
                ted = request.data['taskEndDate']
                dd = None
                rd = None
                if chosen_status > 2:
                    dd = request.data['depart_date']
                    rd = request.data['return_date']
                date_check_result = self.date_check(tsd, ted, dd, rd,
                                                    user_group_name,
                                                    chosen_status)
                if date_check_result['error']:
                    return Response({'error': date_check_result['msg']},
                                    status=status.HTTP_400_BAD_REQUEST)

                if chosen_status == 4:
                    if self.checkAdvancedPetitionCompleteness\
                            (self.get_object().advanced_info) == False:
                        return Response({'error': 'Advanced Petition is'
                                         'not complete,'
                                         'please insert all mandatory fields'
                                         '(missing field:' +
                                         self.missing_field + ')'},
                                        status=status.HTTP_400_BAD_REQUEST)
                return super(UserPetitionViewSet, self).create(request)
            else:
                if self.missing_field is None:
                    return Response({'error': 'Petition is not complete,'
                                    ' please insert all mandatory fields'
                                    ' (missing field:' + "All"
                                    + ')'},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Petition is not complete,'
                                 ' please insert all mandatory fields'
                                 ' (missing field:' + str(self.missing_field)
                                 + ')'},
                                status=status.HTTP_400_BAD_REQUEST)

        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(UserPetitionViewSet, self).create(request)

    def update(self, request, pk=None):
        request.data['user'] = request.user

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

            if self.checkPetitionCompleteness(request, chosen_status):
                tsd = request.data['taskStartDate']
                ted = request.data['taskEndDate']
                dd = None
                rd = None
                if chosen_status > 2:
                    dd = request.data['depart_date']
                    rd = request.data['return_date']
                date_check_result = self.date_check(tsd, ted, dd, rd,
                                                    user_group_name,
                                                    chosen_status)
                if date_check_result['error']:
                    return Response({'error': date_check_result['msg']},
                                    status=status.HTTP_400_BAD_REQUEST)
                if chosen_status == 4:
                    if self.checkAdvancedPetitionCompleteness\
                            (self.get_object().advanced_info) == False:
                        return Response({'error': 'Advanced Petition is'
                                         ' not complete,'
                                         ' please insert all mandatory fields'
                                         ' (missing field:' +
                                         self.missing_field + ')'},
                                        status=status.HTTP_400_BAD_REQUEST)

                return super(UserPetitionViewSet, self).update(request, pk)
            else:
                if self.missing_field is None:
                    return Response({'error': 'Petition is not complete,'
                                    ' please insert all mandatory fields'
                                    ' (missing field:' + "All"
                                    + ')'},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'Petition is not complete,'
                                 ' please insert all mandatory fields'
                                 ' (missing field:' + self.missing_field + ')'},
                                status=status.HTTP_400_BAD_REQUEST)

        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(UserPetitionViewSet, self).update(request, pk)
