from django.db import models

# Create your models here.


class Account(models.Model):

    """Docstring for Account. """
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()


class Specialty(models.Model):

    """Docstring for  Kind. """
    name = models.CharField(max_length=200, primary_key=True)
    kindDescription = models.CharField(max_length=300)

    def __str__(self):
        return self.name + self.kindDescription


class User(models.Model):

    """Docstring for User. """
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)
    accountID = models.ForeignKey(Account, on_delete=models.CASCADE)
    specialtyID = models.ForeignKey(Specialty)
    KIND_CHOICES = (('USER', 'Simple User'), (
        'SECRETARY', 'Secretary'), ('TRAVEL_SUPPORT', 'Travel Support'),
        ('ACCOUNTING', 'Accounting'), ('MANAGER', 'Manager'))
    userKind = models.CharField(
        choices=KIND_CHOICES, max_length=15)
    taxRegNum = models.IntegerField(primary_key=True)
    # itaxOffice = models.CharField(TaxOffice)

    def __str__(self):
        return self.name + "," + self.surname + "," + self.userKind
