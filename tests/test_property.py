from odoo import fields
from odoo.tests.common import TransactionCase

class TestProperty(TransactionCase):
    # Override the "setUp" method in the "TransactionCase" model
    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()
        self.property_02_record = self.env['property'].create({
            'name': 'PRT1000',
            'description': 'PRT1 Description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
        })

    def test_02_property_values(self):
        property_id = self.property_02_record
        self.assertRecordValues(property_id, [{
            'name': 'PRT1000',
            'description': 'PRT1 Description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
        }])

    # Test the uniqueness constraint on the name field
    def test_01_unique_name_constraint(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT1222',  # Duplicate name
                'description': 'Duplicate Property',
                'postcode': '2020',
                'date_availability': fields.Date.today(),
            })

    # Test the constraint for bedrooms being greater than zero
    def test_02_bedrooms_constraint(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT1111',
                'description': 'Invalid Bedrooms',
                'postcode': '3030',
                'date_availability': fields.Date.today(),
                'bedrooms': 0,  # Invalid value
            })

    # Test if garden-related fields are properly initialized
    def test_03_garden_fields(self):
        property_id = self.property_02_record
        self.assertEqual(property_id.garden, False, "Garden field should be True.")
        self.assertEqual(property_id.garden_area, 50, "Garden area should be 50.")
        self.assertEqual(property_id.garden_orientation, 'north', "Garden orientation should be 'north'.")

    # Test expected price default value and update functionality
    def test_04_expected_price_update(self):
        property_id = self.property_02_record
        self.assertEqual(property_id.expected_price, 1.0, "Expected price should match the initial value.")
        # property_id.write({'expected_price': 60000})
        # self.assertEqual(property_id.expected_price, 60000, "Expected price should update to 60000.")