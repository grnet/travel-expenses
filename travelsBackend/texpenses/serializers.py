from models import UserProfile
from models import Specialty
from models import TaxOffice
from rest_framework import serializers


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for User model """

    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'iban',
                  'specialtyID', 'taxRegNum', 'taxOffice')


class SpecialtySerializer(serializers.HyperlinkedModelSerializer):

    """Serializer class for specialty model """

    class Meta:
        model = Specialty
        fields = ('name', 'kindDescription')


class TaxOfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TaxOffice
        fields = ('name', 'kindDescription', 'address', 'email', 'phone')
