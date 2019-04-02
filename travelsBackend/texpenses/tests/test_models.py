
# -*- coding: utf-8 -*-

import pytz
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError, PermissionDenied
from django.test import TestCase, override_settings
from texpenses.models import (Country, City, TravelInfo, Petition,
                              Project,Applications, UserProfile, TaxOffice)


class TravelInfoTest(TestCase):

    def setUp(self):

        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')
        self.user = UserProfile.objects.create(
            first_name='Nick', last_name='Jones', email='test@email.com',
            iban='GR4902603280000910200635494', kind='1',
            specialty='1', tax_reg_num=011111111,
            tax_office=tax_office, user_category='A',
            trip_days_left=5)

        self.base_tz = 'Europe/Athens'

        project = Project.objects.create(name='Test Project',
                                         accounting_code=1,
                                         manager=self.user)

        self.travel_petition = Petition(tax_office=tax_office,status=1,
                                        user_category='A', project=project,
                                        user=self.user)
        self.travel_petition.save()
        self.arrival_country = Country(name='FRANCE', category='A',
                                       currency='EUR')
        self.arrival_country.save()
        self.arrival_point = City(name='PARIS', country=self.arrival_country,
                                  timezone='Europe/Paris')
        self.arrival_point.save()

        self.departure_country = Country(name='GREECE', category='A')
        self.departure_country.save()
        self.departure_point = City(name='ATHENS',
                                    country=self.departure_country,
                                    timezone='Europe/Athens')
        self.departure_point.save()

        self.travel_obj = TravelInfo(accommodation_cost=0.0,
                                     arrival_point=self.arrival_point,
                                     departure_point=self.departure_point,
                                     meals='NON',
                                     travel_petition=self.travel_petition)
        self.travel_obj.save()
        self.travel_petition.travel_info.add(self.travel_obj)
        self.travel_petition.save()

    def test_validate_overnight_cost(self):
        self.travel_obj.validate_overnight_cost(self.travel_petition)
        import copy
        petition = copy.deepcopy(self.travel_petition)

        task_start_date= datetime(2012,9,16,0,0,0,tzinfo=pytz.utc)
        task_end_date= datetime(2012,9,16,0,0,0,tzinfo=pytz.utc)
        return_date= datetime(2012,9,16,0,0,0,tzinfo=pytz.utc)
        depart_date= datetime(2012,9,16,0,0,0,tzinfo=pytz.utc)

        petition.task_start_date = task_start_date
        petition.task_end_date = task_end_date
        travel_info = copy.deepcopy(self.travel_obj)

        travel_info.depart_date = depart_date
        travel_info.return_date = return_date

        travel_info.accommodation_cost = float('inf')
        self.assertRaises(ValidationError,travel_info.validate_overnight_cost,
                          petition)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_transport_days_proposed(self):
        date = datetime.now(pytz.utc)
        self.assertEqual(self.travel_obj.transport_days_proposed(), 0)
        self.travel_obj.depart_date = date
        self.assertEqual(self.travel_obj.transport_days_proposed(), 0)
        self.travel_obj.return_date = date + timedelta(days=7)
        # We remove weekends, that's why six (depart and return counted)
        self.assertEqual(self.travel_obj.transport_days_proposed(), 6)

        self.travel_obj.depart_date = datetime(2012, 9, 12, 21, 10, 0,
                                               tzinfo=pytz.utc)
        self.travel_obj.return_date = datetime(2012, 9, 14, 17, 0, 0,
                                               tzinfo=pytz.utc)
        # 21:10 utc on wed, 12/9, was 00:10 athens time th, 13/9, so 2 days
        self.assertEqual(self.travel_obj.transport_days_proposed(), 2)

        self.travel_obj.depart_date = datetime(2012, 9, 12, 9, 10, 0,
                                               tzinfo=pytz.utc)
        self.travel_obj.return_date = datetime(2012, 9, 14, 17, 0, 0,
                                               tzinfo=pytz.utc)
        self.assertEqual(self.travel_obj.transport_days_proposed(), 3)

        self.travel_obj.depart_date = datetime(2012, 9, 12, 9, 10, 0,
                                               tzinfo=pytz.utc)
        self.travel_obj.return_date = datetime(2012, 9, 16, 17, 0, 0,
                                               tzinfo=pytz.utc)
        # 15 and 16 were sat and sun respectively
        self.assertEqual(self.travel_obj.transport_days_proposed(), 3)


    def test_compensation_level(self):

        self.travel_petition.save()
        self.travel_obj.travel_petition=self.travel_petition

        self.assertEqual(self.travel_obj.compensation_level(), 100)

        arrival_country = Country(name='EGYPT', category='C')
        arrival_country.save()
        arrival_point = City(name='CAIRO', country=arrival_country,
                             timezone='Africa/Cairo')
        arrival_point.save()
        self.travel_obj.arrival_point = arrival_point
        self.assertEqual(self.travel_obj.compensation_level(), 60)

        arrival_country = Country(name='RUSSIA', category='B')
        arrival_country.save()
        arrival_point = City(name='MOSCOW', country=arrival_country,
                             timezone='Europe/Moscow')
        arrival_point.save()
        self.travel_obj.arrival_point = arrival_point
        self.assertEqual(self.travel_obj.compensation_level(), 80)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_same_day_return(self):
        """
        Same day return task should use base timezone for the checks
        """
        travel = self.travel_obj
        travel.travel_petition.task_start_date = datetime(2012, 9, 15, 23, 0, 0,
                                                          tzinfo=pytz.utc)
        travel.depart_date = datetime(2012, 9, 15, 23, 0, 0, tzinfo=pytz.utc)
        travel.travel_petition.task_end_date = datetime(2012, 9, 16, 20, 0, 0,
                                                          tzinfo=pytz.utc)
        travel.return_date = datetime(2012, 9, 16, 20, 0, 0, tzinfo=pytz.utc)
        self.assertTrue(travel.same_day_return_task())

        travel.depart_date -= timedelta(days=1)
        self.assertFalse(self.travel_obj.same_day_return_task())

        travel.depart_date += timedelta(days=1)
        travel.travel_petition.task_start_date -= timedelta(hours=3)
        self.assertFalse(self.travel_obj.same_day_return_task())

    def test_local_depart_date(self):
        self.assertFalse(self.travel_obj.local_depart_date)

        test_date = datetime(2012, 9, 15, 21, 10, 0, tzinfo=pytz.utc)
        self.travel_obj.depart_date = test_date
        local_test_date = datetime(2012, 9, 16).date()
        self.assertEqual(self.travel_obj.local_depart_date.date(),
                         local_test_date)

    def test_local_return_date(self):
        self.assertFalse(self.travel_obj.local_return_date)

        test_date = datetime(2012, 9, 15, 21, 0, 0, tzinfo=pytz.utc)
        self.travel_obj.return_date = test_date
        local_test_date = datetime(2012, 9, 16).date()
        self.assertNotEqual(self.travel_obj.local_return_date.date(),
                            local_test_date)

        self.travel_obj.return_date += timedelta(hours=2)
        self.assertEqual(self.travel_obj.local_return_date.date(),
                         local_test_date)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_base_tz_depart_date(self):
        self.assertFalse(self.travel_obj.base_tz_depart_date)
        test_date = datetime(2012, 9, 15, 21, 10, 0, tzinfo=pytz.utc)
        self.travel_obj.depart_date = test_date
        base_tz_test_date = datetime(2012, 9, 16).date()
        self.assertEqual(self.travel_obj.base_tz_depart_date.date(),
                         base_tz_test_date)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_base_tz_return_date(self):
        self.assertFalse(self.travel_obj.base_tz_return_date)
        test_date = datetime(2012, 9, 15, 21, 10, 0, tzinfo=pytz.utc)
        self.travel_obj.return_date = test_date
        base_tz_test_date = datetime(2012, 9, 16).date()
        self.assertEqual(self.travel_obj.base_tz_return_date.date(),
                         base_tz_test_date)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_overnights_num_proposed(self):
        start_date = datetime.now(pytz.utc)
        end_date = start_date + timedelta(days=7)
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

        self.travel_obj.return_date += timedelta(days=40)
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 9)

        self.travel_obj.depart_date -= timedelta(days=1)
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 9)

        start_date = datetime(2012, 9, 12, 21, 10, 0, tzinfo=pytz.utc)
        end_date = datetime(2012, 9, 14, 17, 0, 0, tzinfo=pytz.utc)
        self.travel_obj.depart_date = start_date
        self.travel_obj.return_date = end_date
        self.assertEqual(self.travel_obj.overnights_num_proposed(
            start_date, end_date), 1)

    def test_is_city_ny(self):
        self.assertFalse(self.travel_obj.is_city_ny())
        city = City(name='ATHENS', country=self.departure_country,
                    timezone='Europe/Athens')
        city.save()
        self.travel_obj.arrival_point = city
        self.assertFalse(self.travel_obj.is_city_ny())
        self.travel_obj.arrival_point.name = 'NEW YORK'

        self.assertTrue(self.travel_obj.is_city_ny())

    def test_clean(self):
        depart = datetime.now(pytz.utc) + timedelta(days=3)
        self.travel_obj.depart_date = depart
        self.travel_obj.return_date = depart + timedelta(days=3)

        self.travel_petition.task_end_date = depart - timedelta(days=2)

        self.assertRaises(ValidationError, self.travel_obj.clean,
                          self.travel_petition)

        self.travel_petition.task_end_date = depart - timedelta(days=4)

        self.assertRaises(ValidationError, self.travel_obj.clean,
                          self.travel_petition)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_compensation_days_proposed(self):
        depart = datetime.now(pytz.utc) + timedelta(days=3)
        return_d = depart + timedelta(days=5)
        task_start = depart + timedelta(days=1)
        task_end = return_d - timedelta(days=1)

        self.travel_obj.depart_date = depart
        self.travel_obj.return_date = return_d

        self.travel_petition.save()
        self.travel_obj.travel_petition=self.travel_petition
        self.travel_obj.travel_petition.task_start_date = task_start
        self.travel_obj.travel_petition.task_end_date = task_end

        overnights = self.travel_obj.overnights_num_proposed(
            task_start, task_end)
        self.travel_obj.compensation_days_manual = overnights
        self.assertEqual(self.travel_obj.compensation_days_proposed(), 5)

        start_date = datetime(2012, 9, 12, 21, 10, 0, tzinfo=pytz.utc)
        end_date = datetime(2012, 9, 14, 17, 0, 0, tzinfo=pytz.utc)
        self.travel_obj.depart_date = start_date
        self.travel_obj.return_date = None
        self.travel_petition.task_start_date = start_date
        self.travel_petition.task_end_date = end_date
        self.assertEqual(self.travel_obj.compensation_days_proposed(), 0)

        self.travel_obj.return_date = end_date
        self.assertEqual(self.travel_obj.compensation_days_proposed(), 2)

        self.travel_obj.return_date = start_date
        self.travel_petition.task_end_date = start_date
        self.assertEqual(self.travel_obj.compensation_days_proposed(), 1)

    def test_is_athens_or_thesniki(self):
        self.assertFalse(self.travel_obj.is_athens_or_thesniki())

        self.travel_obj.arrival_point = None
        self.assertFalse(self.travel_obj.is_athens_or_thesniki())

        greece = Country(name=u'Ελλάδα', category='B')
        city = City(name=u'Χανιά', country=greece)
        self.travel_obj.arrival_point = city
        self.assertFalse(self.travel_obj.is_athens_or_thesniki())

        self.travel_obj.arrival_point.name = u'Αθήνα'
        self.assertTrue(self.travel_obj.is_athens_or_thesniki())

        self.travel_obj.arrival_point.name = u'Θεσσαλονίκη'
        self.assertTrue(self.travel_obj.is_athens_or_thesniki())

    def test_is_abroad(self):
        self.assertTrue(self.travel_obj.is_abroad())

        self.travel_obj.arrival_point = None
        self.assertTrue(self.travel_obj.is_abroad())

        greece = Country(name=u'Ελλάδα', category='B')
        city = City(name=u'Χανιά', country=greece)
        self.travel_obj.arrival_point = city
        self.assertFalse(self.travel_obj.is_abroad())

        self.travel_obj.arrival_point.country.name = u'Γαλλία'
        self.assertTrue(self.travel_obj.is_abroad())

    def test_transport_car_or_bike(self):
        self.assertFalse(self.travel_obj.means_of_transport_is_car_or_bike())

        self.travel_obj.means_of_transport = 'BIKE'
        self.assertTrue(self.travel_obj.means_of_transport_is_car_or_bike())

        self.travel_obj.means_of_transport = 'CAR'
        self.assertTrue(self.travel_obj.means_of_transport_is_car_or_bike())

        self.travel_obj.means_of_transport = 'SHIP'
        self.assertFalse(self.travel_obj.means_of_transport_is_car_or_bike())

    def test_transport_train_ship_bus(self):
        self.assertFalse(self.travel_obj.means_of_transport_is_train_ship_bus())

        self.travel_obj.means_of_transport = 'BIKE'
        self.assertFalse(self.travel_obj.means_of_transport_is_train_ship_bus())

        self.travel_obj.means_of_transport = 'CAR'
        self.assertFalse(self.travel_obj.means_of_transport_is_train_ship_bus())

        self.travel_obj.means_of_transport = 'SHIP'
        self.assertTrue(self.travel_obj.means_of_transport_is_train_ship_bus())

        self.travel_obj.means_of_transport = 'TRAIN'
        self.assertTrue(self.travel_obj.means_of_transport_is_train_ship_bus())

        self.travel_obj.means_of_transport = 'BUS'
        self.assertTrue(self.travel_obj.means_of_transport_is_train_ship_bus())

    def test_transportation_should_be_compensated(self):
        self.assertFalse(self.travel_obj.transportation_should_be_compensated())

        self.travel_obj.means_of_transport = 'CAR'
        self.assertTrue(self.travel_obj.transportation_should_be_compensated())

        self.travel_obj.means_of_transport = 'BIKE'
        self.assertTrue(self.travel_obj.transportation_should_be_compensated())

        self.travel_obj.transportation_payment_way = u'GRNET'
        self.travel_obj.means_of_transport = 'TRAIN'
        self.assertFalse(self.travel_obj.transportation_should_be_compensated())

        self.travel_obj.transportation_payment_way = u'VISA'
        self.assertTrue(self.travel_obj.transportation_should_be_compensated())

    def test_transportation_cost_should_be_calculated(self):
        travel = self.travel_obj
        self.assertFalse(travel.transportation_cost_should_be_calculated())

        travel.means_of_transport = 'BIKE'
        self.assertTrue(travel.transportation_cost_should_be_calculated())

        travel.means_of_transport = 'CAR'
        self.assertTrue(travel.transportation_cost_should_be_calculated())

        travel.no_transportation_calculation = True
        self.assertFalse(travel.transportation_cost_should_be_calculated())

    def test_save_and_transport_cost_calculation(self):
        travel = self.travel_obj
        travel.transportation_cost = 300
        travel.save()
        self.assertEqual(travel.transportation_cost, 300)

        travel.means_of_transport = 'CAR'
        travel.save()
        # assert cost 0 because there's no distance in calculation
        self.assertEqual(travel.transportation_cost, 0)

        travel.transportation_cost = 300
        travel.no_transportation_calculation = True
        travel.save()
        self.assertEqual(travel.transportation_cost, 300)


class PetitionTest(TestCase):

    end_date = datetime(2012, 9, 16, 21, 10, 0, tzinfo=pytz.utc)
    start_date = end_date - timedelta(days=1)

    def setUp(self):
        tax_office = TaxOffice.objects.create(
            name='test', description='test', address='test',
            email='test@example.com', phone='2104344444')

        self.user = UserProfile.objects.create(
            first_name='Nick', last_name='Jones', email='test@email.com',
            iban='GR4902603280000910200635494', kind='1',
            specialty='1', tax_reg_num=011111111,
            tax_office=tax_office, user_category='A',
            trip_days_left=5)

        departure_city = City.objects.create(
            name='Athens', country=Country.objects.create(name='Greece'),
            timezone='Europe/Athens')
        arrival_city = City.objects.create(
            name='Paris', country=Country.objects.create(name='France'),
            timezone='Europe/Paris')
        self.project = Project.objects.create(name='Test Project',
                                              accounting_code=1,
                                              manager=self.user)
        self.petition = Petition.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            status=1, user=self.user, project=self.project)

        self.travel_info = TravelInfo.objects.create(
            return_date=self.end_date, depart_date=self.start_date,
            accommodation_cost=10,
            transport_days_manual=4,
            overnights_num_manual=4,
            arrival_point=arrival_city,
            departure_point=departure_city,
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
        for travel in self.petition.travel_info.all():
            travel.delete()
        self.petition.delete()
        self.assertRaises(Petition.DoesNotExist, Petition.objects.get,
                id=self.petition.id)

    def test_mark_as_deleted(self):
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertEqual(self.petition.status, 1)
        self.petition.mark_as_deleted()
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertTrue(petition.deleted)
        self.petition.unmark_deleted()
        petition = Petition.objects.get(id=self.petition.id)
        self.assertIsNotNone(petition)
        self.assertFalse(petition.deleted)

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

    def test_local_task_start_date(self):
        local_test_date = datetime(2012, 9, 15).date()
        self.assertEqual(self.petition.local_task_start_date.date(),
                         local_test_date)

        self.petition.task_start_date = None
        self.assertFalse(self.petition.local_task_start_date)

    def test_local_task_end_date(self):
        local_test_date = datetime(2012, 9, 16).date()
        self.assertEqual(self.petition.local_task_end_date.date(),
                         local_test_date)

        self.petition.task_end_date = None
        self.assertFalse(self.petition.local_task_end_date)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_base_tz_task_start_date(self):
        base_tz_test_date = datetime(2012, 9, 16).date()
        self.assertEqual(self.petition.base_tz_task_start_date.date(),
                         base_tz_test_date)

        self.petition.task_start_date = None
        self.assertFalse(self.petition.base_tz_task_start_date)

    @override_settings(BASE_TIMEZONE='Europe/Athens')
    def test_base_tz_task_end_date(self):
        base_tz_test_date = datetime(2012, 9, 17).date()
        self.assertEqual(self.petition.base_tz_task_end_date.date(),
                         base_tz_test_date)

        self.petition.task_end_date = None
        self.assertFalse(self.petition.base_tz_task_end_date)

    def test_status_transition(self):
        data = {
            'project': self.project,
            'user': self.user,
            'status': Petition.SUBMITTED_BY_USER,
        }
        petition = Petition.objects.create(**data)
        sub_petition_id = petition.id
        travel_info = TravelInfo.objects.create(travel_petition=petition)
        petition.travel_info.add(travel_info)
        self.assertFalse(petition.deleted)
        self.assertRaises(PermissionDenied, petition.status_transition,
                          petition.SUBMITTED_BY_USER)
        petition_id = petition.status_transition(petition.SAVED_BY_USER)
        self.assertNotEqual(petition_id, sub_petition_id)
        self.assertFalse(petition.deleted)
        self.assertEqual(petition.status, Petition.SAVED_BY_USER)

        previous_petition = Petition.objects.get(id=sub_petition_id)
        self.assertTrue(previous_petition.deleted)
        previous_travel_info = previous_petition.travel_info.all()
        current_travel_info = petition.travel_info.all()

        self.assertEqual(len(previous_travel_info), len(current_travel_info))
        for i, travel_obj in enumerate(current_travel_info):
            self.assertNotEqual(travel_obj.id, previous_travel_info[i].id)
            self.assertNotEqual(travel_obj.travel_petition,
                                previous_travel_info[i].travel_petition)
        previous_petition.deleted = False
        previous_petition.status = Petition.SAVED_BY_SECRETARY
        previous_petition.save()
        self.assertRaises(
            PermissionDenied,
            petition.status_transition, Petition.SAVED_BY_USER)

    def test_application(self):
        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=1)
        self.assertEqual(petition.status, Petition.SAVED_BY_USER)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=2)
        self.assertEqual(petition.status, Petition.SUBMITTED_BY_USER)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=3)
        self.assertEqual(petition.status, Petition.SAVED_BY_SECRETARY)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=4)
        self.assertEqual(petition.status,
                         Petition.SUBMITTED_BY_SECRETARY)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=5)
        self.assertEqual(petition.status,
                         Petition.APPROVED_BY_PRESIDENT)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=6)
        self.assertEqual(petition.status,
                         Petition.USER_COMPENSATION)
        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=7)
        self.assertEqual(petition.status,
                         Petition.USER_COMPENSATION_SUBMISSION)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=8)
        self.assertEqual(petition.status,
                         Petition.SECRETARY_COMPENSATION)

        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=9)
        self.assertEqual(petition.status,
                         Petition.SECRETARY_COMPENSATION_SUBMISSION)
        petition = Applications.objects.create(
            task_start_date=self.start_date, task_end_date=self.end_date,
            user=self.user, project=self.project, status=10)
        self.assertEqual(petition.status,
                         Petition.PETITION_FINAL_APPOVAL)

