from django.db import models
from django.contrib.auth.models import User
from validators import iban_validation
from validators import afm_validator


class Specialty(models.Model):

    """Docstring for  Kind. """
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class TaxOffice(models.Model):

    """Docstring for TaxOffice. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    """Docstring for User. """
    # id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=200)
    # surname = models.CharField(max_length=200)
    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=True, null=True)

    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s's profile" % self.user
