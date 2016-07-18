from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.models import (
    City, TravelInfo, Petition, UserPetition, Project, UserProfile, TaxOffice,
    UserPetitionSubmission, SecretaryPetition, SecretaryPetitionSubmission)


class TravelInfoTest(TestCase):
    def setUp(self):
        travel_petition = Petition(category='A')
        self.travel_obj = TravelInfo(travel_petition=travel_petition,
                                     accommodation_price=0.0)

    def test_validate_overnight_cost(self):
        self.travel_obj.validate_overnight_cost()
        self.travel_obj.accommodation_price = float('inf')
        self.assertRaises(ValidationError,
                          self.travel_obj.validate_overnight_cost)

    def test_transport_days_proposed(self):
        date = datetime.now()
        self.assertEqual(self.travel_obj.transport_days_proposed(), 0)
        self.travel_obj.depart_date = date
        self.assertEqual(self.travel_obj.transport_days_proposed(), 0)
        self.travel_obj.return_date = date + timedelta(days=7)
        # We remove weekends, that's why five.
        self.assertEqual(self.travel_obj.transport_days_proposed(), 5)

    def test_overnights_num_proposed(self):
        end_date = datetime.now()
        start_date = datetime.now() - timedelta(days=7)
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 0)

        self.travel_obj.return_date = end_date
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 0)

        self.travel_obj.depart_date = start_date
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 7)

        self.travel_obj.return_date += timedelta(days=1)
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 8)

        self.travel_obj.depart_date -= timedelta(days=1)
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 9)

    def test_is_city_ny(self):
        self.assertFalse(self.travel_obj.is_city_ny())
        city = City(name='ATHENS')
        self.travel_obj.arrival_point = city
        self.assertFalse(self.travel_obj.is_city_ny())
        self.travel_obj.arrival_point.name = 'NEW YORK'
        self.assertTrue(self.travel_obj.is_city_ny())


class PetitionTest(TestCase):

    end_date = datetime.now() + timedelta(days=10)
    start_date = end_date - timedelta(days=1)

    def setUp(self):
        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')
        self.user = UserProfile.objects.create(
            first_name='Nick', last_name='Jones', email='test@email.com',
            iban='GR4902603280000910200635494',
            specialty='1', tax_reg_num=150260153,
            tax_office=tax_office, category='A',
            trip_days_left=5)
        city = City.objects.create(name='Athens')
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1)
        self.petition = Petition.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            status=1, user=self.user, project=self.project)
        self.travel_info = TravelInfo.objects.create(
            return_date=self.end_date, depart_date=self.start_date,
            accommodation_price=10,
            transport_days_manual=4,
            overnights_num_manual=4,
            arrival_point=city,
            departure_point=city,
            travel_petition=self.petition)
        self.petition.travel_info.add(self.travel_info)

    def test_user_info(self):
        for field in Petition.USER_FIELDS:
            self.assertEqual(getattr(self.petition, field),
                             getattr(self.user, field))

    def test_delete(self):
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertEqual(self.petition.status, 1)
        self.petition.delete()
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertEqual(self.petition.status, Petition.DELETED)

    def test_set_next_dse(self):
        petition = Petition.objects.get(id=self.petition.id)
        self.assertEqual(petition.dse, 1)
        petition.set_next_dse()
        self.assertEqual(petition.dse, 2)

    def test_task_duration(self):
        self.assertEqual(self.petition.task_duration(), 1)

        self.petition.task_start_date = None
        self.assertEqual(self.petition.task_duration(), 0)

        self.petition.task_start_date = self.start_date
        self.petition.task_end_date = None
        self.assertEqual(self.petition.task_duration(), 0)

    def test_user_petition_manager(self):
        user_petition = UserPetition.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project)
        self.assertEqual(user_petition.status, Petition.SAVED_BY_USER)
        self.petition.status = Petition.DELETED
        self.petition.save()
        for petition in UserPetition.objects.all():
            self.assertEqual(petition.status, Petition.SAVED_BY_USER)

    def test_user_submission_manager(self):
        user_petition = UserPetitionSubmission.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project)
        self.assertEqual(user_petition.status, Petition.SUBMITTED_BY_USER)
        for petition in UserPetitionSubmission.objects.all():
            self.assertEqual(petition.status, Petition.SUBMITTED_BY_USER)

    def test_secretary_petition_manager(self):
        user_petition = SecretaryPetition.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project)
        self.assertEqual(user_petition.status, Petition.SAVED_BY_SECRETARY)
        for petition in SecretaryPetition.objects.all():
            self.assertEqual(petition.status, Petition.SAVED_BY_SECRETARY)

    def test_secretary_petition_submission_manager(self):
        user_petition = SecretaryPetitionSubmission.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project)
        self.assertEqual(user_petition.status, Petition.SUBMITTED_BY_SECRETARY)
        for petition in SecretaryPetitionSubmission.objects.all():
            self.assertEqual(petition.status, Petition.SUBMITTED_BY_SECRETARY)

    def test_petition_submission(self):
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertEqual(petition.status, Petition.SAVED_BY_USER)

        UserPetitionSubmission.objects.create(
            dse=petition.dse,
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project)

        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertEqual(petition.status, Petition.DELETED)
