from django.db import models
from django.contrib.auth.models import User

# class Account(models.Model):

    # """Docstring for Account. """
    # username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    # email = models.EmailField()
    # id = models.AutoField(primary_key=True)
    # tokken = models.CharField(max_length=100)

    # def __str__(self):
        # return self.username


class Specialty(models.Model):

    """Docstring for  Kind. """
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class UserKind(models.Model):

    """Docstring for User Kind. """
    name = models.CharField(max_length=200)
    kindDescription = models.CharField(max_length=300)
    id = models.AutoField(primary_key=True)

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


class UserProfile(models.Model):

    """Docstring for User. """
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)
    specialtyID = models.ForeignKey(Specialty)
    userKind = models.ForeignKey(UserKind)
    taxRegNum = models.IntegerField(
        primary_key=True)
    taxOffice = models.ForeignKey(TaxOffice)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s's profile" % self.user
