from models import UserProfile
from models import Specialty
from models import UserKind
from models import TaxOffice
from serializers import UserProfileSerializer
from serializers import SpecialtySerializer
from serializers import UserKindSerializer
from serializers import TaxOfficeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication,\
    TokenAuthentication
from custom_permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):

    """API endpoint that allows users model to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin, )

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class SpecialtyViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """

    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class UserKindViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)
    queryset = UserKind.objects.all()
    serializer_class = UserKindSerializer


class TaxOfficeViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAdminUser,)
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer
