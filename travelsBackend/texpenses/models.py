from django.db import models
from django.contrib.auth.models import AbstractUser
from validators import iban_validation
from validators import afm_validator


class Specialty(models.Model):

    """Docstring for Specialty . """
    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name


class Kind(models.Model):

    """Docstring for Kind. """

    name = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

    def __unicode__(self):
        return self.name


class TaxOffice(models.Model):

    """Docstring for TaxOffice. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class UserProfile(AbstractUser):
    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=True, null=True)
    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)


class Accomondation(models.Model):

    """Docstring for Accomondation. """
    id = models.AutoField(primary_key=True)
    hotel = models.CharField(max_length=200)
    hotelPrice = models.FloatField(blank=True, null=True)
    checkInDate = models.DateField(blank=True, null=True)
    checkOutDate = models.DateField(blank=True, null=True)


class Project(models.Model):

    """Docstring for Project. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    accountingCode = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class MovementCategories(models.Model):

    """Docstring for MovementCategories. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class DeparturePoint(models.Model):

    """Docstring for DeparturePoint. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class ArrivalPoint(models.Model):

    """Docstring for ArrivalPoint. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class Transportation(models.Model):

    """Docstring for Transportation. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class PetitionStatus(models.Model):

    """Docstring for Petition status. """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        """TODO: to be defined1. """
        return self.name


class Petition(models.Model):

    """Docstring for Travel Application. """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    surname = models.CharField(max_length=200, blank=True, null=True)
    iban = models.CharField(max_length=200, blank=True, null=True,
                            validators=[iban_validation])
    specialtyID = models.ForeignKey(Specialty, blank=True, null=True)
    taxRegNum = models.IntegerField(blank=True, null=True,
                                    validators=[afm_validator])
    taxOffice = models.ForeignKey(TaxOffice, blank=True, null=True)
    kind = models.ForeignKey(Kind, blank=True, null=True)

    user = models.ForeignKey(UserProfile)
    accomondation = models.ForeignKey(Accomondation, blank=True, null=True)
    taskStartDate = models.DateTimeField(blank=True, null=True)
    taskEndDate = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(Project)
    reason = models.CharField(max_length=500, blank=True, null=True)
    movementCategory = models.ForeignKey(
        MovementCategories, blank=True, null=True)
    departurePoint = models.ForeignKey(DeparturePoint, blank=True, null=True)
    arrivalPoint = models.ForeignKey(ArrivalPoint, blank=True, null=True)
    transportation = models.ForeignKey(Transportation, blank=True, null=True)
    recTransport = models.CharField(max_length=200, blank=True, null=True)
    recAccomondation = models.CharField(max_length=200, blank=True, null=True)
    recCostParticipation = models.CharField(
        max_length=200, blank=True, null=True)
    status = models.ForeignKey(PetitionStatus, blank=True, null=True)

    def __unicode__(self):
        return str(self.id) + "-" + self.project.name
