from models import UserProfile
# from models import Account
from models import Specialty
from models import UserKind
from models import TaxOffice
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for User model """

    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'iban', 'accountID',
                  'specialtyID', 'userKind', 'taxRegNum', 'taxOffice')


# class AccountSerializer(serializers.HyperlinkedModelSerializer):

    # """Serializer class for Account model """

    # class Meta:
        # model = Account
        # fields = ('username', 'password', 'email', 'id', 'tokken')


class SpecialtySerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for specialty model """

    class Meta:
        model = Specialty
        fields = ('name', 'kindDescription')


class UserKindSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for user kind model """

    class Meta:
        model = UserKind
        fields = ('name', 'kindDescription')


class TaxOfficeSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for user kind model """

    class Meta:
        model = TaxOffice
        fields = ('name', 'kindDescription', 'address', 'email', 'phone')
