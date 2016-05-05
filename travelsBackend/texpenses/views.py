import requests
import urllib
import logging
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from djoser import views as djoser_views
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication

from rest_framework_tracking.mixins import LoggingMixin
from models import Specialty
from models import TaxOffice
from models import Kind
from models import Petition
from models import Accomondation
from models import Project
from models import MovementCategories
from models import DeparturePoint
from models import ArrivalPoint
from models import Transportation
from models import PetitionStatus

from serializers import UserProfileSerializer
from serializers import SpecialtySerializer
from serializers import TaxOfficeSerializer
from serializers import KindSerializer
from serializers import CustomUserRegistrationSerializer
from serializers import AccomondationSerializer
from serializers import ArrivalPointSerializer
from serializers import DeparturePointSerializer
from serializers import MovementCategoriesSerializer
from serializers import ProjectSerializer
from serializers import TransportationSerializer
from serializers import UserPetitionSerializer
from serializers import PetitionStatusSerializer
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
    pass


class CustomActivationView(LoggingMixin, djoser_views.ActivationView):
    pass


class CustomSetUsernameView(LoggingMixin, djoser_views.SetUsernameView):
    pass


class CustomSetPasswordView(LoggingMixin, djoser_views.SetPasswordView):
    pass


class CustomPasswordResetView(LoggingMixin, djoser_views.PasswordResetView):
    pass


class CustomPasswordResetConfirmView(LoggingMixin,
                                     djoser_views.PasswordResetConfirmView):
    pass


class CustomLoginView(LoggingMixin, djoser_views.LoginView):
    pass


class CustomLogoutView(LoggingMixin, djoser_views.LogoutView):
    pass


class CustomRootView(LoggingMixin, djoser_views.RootView):
    pass


class CustomUserDetailedView(LoggingMixin, djoser_views.UserView):

    serializer_class = UserProfileSerializer
    permission_classes = (
        IsAuthenticated, DjangoModelPermissions,
    )
    queryset = User.objects.all()


class SpecialtyViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class KindViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class TaxOfficeViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer


class CustomUserRegistrationView(LoggingMixin, djoser_views.RegistrationView):
    serializer_class = CustomUserRegistrationSerializer


class AccomondationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows accomondation details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Accomondation.objects.all()
    serializer_class = AccomondationSerializer


class ProjectViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows project details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MovementCategoriesViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows movement  details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = MovementCategories.objects.all()
    serializer_class = MovementCategoriesSerializer


class DeparturePointViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows departure point to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = DeparturePoint.objects.all()
    serializer_class = DeparturePointSerializer


class ArrivalPointViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows arrival point to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = ArrivalPoint.objects.all()
    serializer_class = ArrivalPointSerializer


class TransportationViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows transportation to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer


class PetitionStatusViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows transportation to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (
        IsAuthenticated, isAdminOrRead, DjangoModelPermissions,)
    queryset = PetitionStatus.objects.all()
    serializer_class = PetitionStatusSerializer


class UserPetitionViewSet(LoggingMixin, viewsets.ModelViewSet):

    """API endpoint that allows transportation to be viewed or edited """
    petition_status = "http://127.0.0.1:8000/petition/petition_status/2/"

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

        values = request.data.values()

        if None in values or '' in values:
            return False

        return True

    def create(self, request):
        request.data['user'] = request.user
        print request.data

        # return super(UserPetitionViewSet, self).create(request)
        chosen_status = request.data['status']
        print "Chosen status:" + str(chosen_status)
        if chosen_status == self.petition_status:
            if self.checkDataCompleteness(request):
                return super(UserPetitionViewSet, self).create(request)
            else:
                return Response({'error': 'Petition is not complete,\
                                 please insert all mandatory fields'},
                                status=status.HTTP_400_BAD_REQUEST)
        if chosen_status is None:
            return Response({'error': 'Petition status is not set'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super(UserPetitionViewSet, self).create(request)
