from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from texpenses.models import City, TravelInfo, Petition


class TravelInfoTest(TestCase):
    def setUp(self):
        travel_petition = Petition(category='A')
        self.travel_obj = TravelInfo(travel_petition=travel_petition,
                                     accomondation_price=0.0)

    def test_validate_overnight_cost(self):
        self.travel_obj.validate_overnight_cost()
        self.travel_obj.accomondation_price = float('inf')
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
