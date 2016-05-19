import requests
import urllib
import logging
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser import views as djoser_views
from django.db.utils import OperationalError
from django.core.exceptions import ObjectDoesNotExist
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
        url = 'http://localhost:8000/auth/activate/'
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

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_staff:
            return Accomondation.objects.all()
        else:
            return Accomondation.objects.filter(user=request_user)
    serializer_class = AccomondationSerializer


class AdvancedPetitionViewSet(LoggingMixin, mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet
                              ):

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_staff:
            return AdvancedPetition.objects.all()
        else:
            return AdvancedPetition.objects.filter(user=request_user)
    serializer_class = AdvancedPetitionSerializer

    def update(self, request, pk=None):
        dd = request.data['depart_date']
        rd = request.data['return_date']
        if rd < dd:
            return Response(
                {'error': 'Return date should be after departure date'},
                status=status.HTTP_400_BAD_REQUEST)
        return super(AdvancedPetitionViewSet, self).update(request, pk)

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

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_staff:
            return Flight.objects.all()
        else:
            return Flight.objects.filter(user=request_user)
    serializer_class = FlightSerializer


class CompensationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Compensation.objects.all()
    serializer_class = CompensationSerializer


class AdditionalExpensesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, IsOwnerOrAdmin, DjangoModelPermissions,)

    def get_queryset(self):
        request_user = self.request.user
        if request_user.is_staff:
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

    """API endpoint that allows petition statuses to be viewed or edited \
        (permissions are needed)"""
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = FeedingKind.objects.all()
    serializer_class = FeedingKindSerializer


class UserPetitionViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows user related petitions to be viewed or edited \
        (permissions are needed)"""
    # petition_status = "http://127.0.0.1:8000/petition/petition_status/2/"
    missing_field = None
    try:

        petition_status_2 = str(PetitionStatus.objects.get(id='2').id)
    except OperationalError:
        pass
    except ObjectDoesNotExist:
        pass

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,
                          DjangoModelPermissions,)

    filter_backends = (filters.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter,)
    filter_fields = ('taskStartDate', 'taskEndDate', 'project',
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
        if request_user.is_staff:
            return Petition.objects.all()
        else:
            return Petition.objects.filter(user=request_user)

    serializer_class = UserPetitionSerializer

    def checkDataCompleteness(self, request):
        """TODO: Docstring for checkDataCompleteness.

        :request: TODO
        :returns: TODO

        """
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
            project = request.data['project']
            reason = request.data['reason']
            movementCategory = request.data['movementCategory']
            departurePoint = request.data['departurePoint']
            arrivalPoint = request.data['arrivalPoint']
            transportation = request.data['transportation']
        except KeyError:
            print "Shit"
            return False

        none_mandatory_fields = ['accomondation', 'recCostParticipation']
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

    def destroy(self, request, pk=None):

        petition = self.get_object()
        pet_status = petition.status.id
        petition_status_to_delete = 1

        if pet_status == petition_status_to_delete:
            print "Deleting petition with id:" + str(pk)

            advanced_petition = petition.advanced_info

            print "--Deleting related Advanced\
                Petition with id:" + str(advanced_petition.id)
            advanced_petition.delete()
            print "----Deleting related flight:" + str(advanced_petition.flight)
            advanced_petition.flight.delete()
            print "----Done"

            print "----Deleting related accomondation:\
                  " + str(advanced_petition.accomondation)
            advanced_petition.accomondation.delete()
            print "----Done"
            print "--Done"
            petition.delete()
            print "Done"

            return Response(status=status.HTTP_204_NO_CONTENT)
            # return super(UserPetitionViewSet, self).destroy(request, pk)

        return Response({'error': "You dont have the permittions to delete \
                         the specific Petition"},
                        status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        request.data['user'] = request.user

        chosen_status = str(request.data['status'])

        chosen_status = chosen_status[
            chosen_status.index('status') + 7:-1]

        if chosen_status == self.petition_status_2:

            tsd = request.data['taskStartDate']
            ted = request.data['taskEndDate']

            if ted < tsd:
                return Response(
                    {'error': 'Task end date should be after task start date'},
                    status=status.HTTP_400_BAD_REQUEST)

            if self.checkDataCompleteness(request):
                return super(UserPetitionViewSet, self).create(request)
            else:
                return Response({'error': 'Petition is not complete,\
                                 please insert all mandatory fields\
                                 (missing field:' + self.missing_field + ')'},
                                status=status.HTTP_400_BAD_REQUEST)
        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(UserPetitionViewSet, self).create(request)

    def update(self, request, pk=None):
        request.data['user'] = request.user

        petition = self.get_object()
        chosen_status = petition.status.id
        chosen_status = str(chosen_status)

        now = datetime.today()

        if chosen_status == self.petition_status_2:
            tsd = petition.taskStartDate
            ted = petition.taskEndDate

            if tsd < now:
                return Response(
                    {'error': 'Task start date should be after today'},
                    status=status.HTTP_400_BAD_REQUEST)
            if ted < now:
                return Response(
                    {'error': 'Task end date should be after today'},
                    status=status.HTTP_400_BAD_REQUEST)
            if ted < tsd:
                return Response(
                    {'error': 'Task end date should be after task start date'},
                    status=status.HTTP_400_BAD_REQUEST)

            if self.checkDataCompleteness(request):
                return super(UserPetitionViewSet, self).update(request, pk)
            else:
                return Response({'error': 'Petition is not complete,\
                                 please insert all mandatory fields\
                                 (missing field:' + self.missing_field + ')'},
                                status=status.HTTP_400_BAD_REQUEST)
        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(UserPetitionViewSet, self).update(request, pk)
