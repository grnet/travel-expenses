from django.core.management import call_command
from django.test import TestCase
from django.core.management.base import CommandError
from django.conf import settings

from texpenses.models import (Country, City, Project, TaxOffice, UserProfile,
                              UserDaysLeft)


class LoadLocationsTest(TestCase):
    def test_command_no_arguments(self):
        with self.assertRaises(CommandError):
            call_command('loadlocations')

    def test_command_wrong_file(self):
        with self.assertRaises(IOError):
            call_command('loadlocations', 'file_not_existing.csv')

    def test_correct_command(self):
        countries_before = Country.objects.count()
        cities_before = City.objects.count()
        call_command('loadlocations', 'texpenses/data/countriesTZ.csv')
        countries_after = Country.objects.count()
        cities_after = City.objects.count()
        self.assertGreater(countries_after, countries_before)
        self.assertGreater(cities_after, cities_before)


class LoadProjectsTest(TestCase):
    def test_command_no_arguments(self):
        with self.assertRaises(CommandError):
            call_command('loadprojects')

    def test_command_wrong_file(self):
        with self.assertRaises(IOError):
            call_command('loadprojects', 'file_not_existing.csv')

    def test_correct_command(self):
        projects_before = Project.objects.count()
        call_command('loadprojects', 'texpenses/data/ListProjects.csv')
        projects_after = Project.objects.count()
        self.assertGreater(projects_after, projects_before)


class LoadTaxOfficesTest(TestCase):
    def test_command_no_arguments(self):
        with self.assertRaises(CommandError):
            call_command('loadtaxoffices')

    def test_command_wrong_file(self):
        with self.assertRaises(IOError):
            call_command('loadtaxoffices', 'file_not_existing.csv')

    def test_correct_command(self):
        taxoffices_before = TaxOffice.objects.count()
        call_command('loadtaxoffices', 'texpenses/data/ListEfories.csv')
        taxoffices_after = TaxOffice.objects.count()
        self.assertGreater(taxoffices_after, taxoffices_before)


class ResetTravelDaysTest(TestCase):
    def setUp(self):
        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')

        self.user = UserProfile.objects.create(
            first_name='Nick', last_name='Jones', email='test@email.com',
            iban='GR4902603280000910200635494', kind='1',
            specialty='1', tax_reg_num='011111111',
            tax_office=tax_office, user_category='A',
            trip_days_left=5)
        self.user.save()

    def test_command(self):
        call_command('resettraveldays')
        records_created = UserDaysLeft.objects.count()
        self.assertEqual(records_created, 1)

        record = UserDaysLeft.objects.get(user=self.user)
        self.assertEqual(record.days_left, 5)
        u = UserProfile.objects.get(username=self.user.username)
        self.assertEqual(u.trip_days_left, settings.MAX_HOLIDAY_DAYS)

        # Test that second reset does nothing
        u.trip_days_left -= 1
        u.save()
        call_command('resettraveldays')
        records = UserDaysLeft.objects.count()
        self.assertEqual(records, 1)

        record = UserDaysLeft.objects.get(user=self.user)
        self.assertEqual(record.days_left, 5)
        u = UserProfile.objects.get(username=self.user.username)
        self.assertEqual(u.trip_days_left, settings.MAX_HOLIDAY_DAYS - 1)
