from django.db import models
from validators import iban_validation


class Account(models.Model):

    """Docstring for Account. """
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Specialty(models.Model):

    """Docstring for  Kind. """
    name = models.CharField(max_length=200, primary_key=True)
    kindDescription = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class UserKind(models.Model):

    """Docstring for User Kind. """
    name = models.CharField(max_length=200, primary_key=True)
    kindDescription = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class TaxOffice(models.Model):

    """Docstring for TaxOffice. """
    name = models.CharField(max_length=200, primary_key=True)
    kindDescription = models.CharField(max_length=300)
    address = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(models.Model):

    """Docstring for User. """
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    iban = models.CharField(max_length=200, validators=[iban_validation])
    accountID = models.ForeignKey(Account, on_delete=models.CASCADE)
    specialtyID = models.ForeignKey(Specialty)
    userKind = models.ForeignKey(UserKind)
    # KIND_CHOICES = (('USER', 'Simple User'), (
    # 'SECRETARY', 'Secretary'), ('TRAVEL_SUPPORT', 'Travel Support'),
    # ('ACCOUNTING', 'Accounting'), ('MANAGER', 'Manager'))
    # userKind = models.CharField(
    # choices=KIND_CHOICES, max_length=15)
    taxRegNum = models.IntegerField(primary_key=True)
    taxOffice = models.ForeignKey(TaxOffice)

    def __str__(self):
        return self.name + "," + self.surname + "," + self.userKind
