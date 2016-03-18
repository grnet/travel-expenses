from models import UserProfile
# from models import Account
from models import Specialty
from models import UserKind
from models import TaxOffice
from serializers import UserSerializer
# from serializers import AccountSerializer
from serializers import SpecialtySerializer
from serializers import UserKindSerializer
from serializers import TaxOfficeSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):

    """API endpoint that allows users model to be viewed or edited """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


# class AccountViewSet(viewsets.ModelViewSet):

    # """API endpoint that allows account details to be viewed or edited """
    # queryset = Account.objects.all()
    # serializer_class = AccountSerializer


class SpecialtyViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer


class UserKindViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    queryset = UserKind.objects.all()
    serializer_class = UserKindSerializer


class TaxOfficeViewSet(viewsets.ModelViewSet):

    """API endpoint that allows specialty details to be viewed or edited """
    queryset = TaxOffice.objects.all()
    serializer_class = TaxOfficeSerializer
