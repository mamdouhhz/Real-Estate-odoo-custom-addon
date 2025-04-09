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

    def test_01_property_values(self):
        property_id = self.property_02_record
        self.assertRecordValues(property_id, [{
            'name': 'PRT1000',
            'description': 'PRT1 Description',
            'postcode': '1010',
            'date_availability': fields.Date.today(),
        }])

    # Test the uniqueness constraint on the name field
    def test_02_unique_name_constraint(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT1000',  # Duplicate name
                'description': 'Duplicate Property',
                'postcode': '2020',
                'date_availability': fields.Date.today(),
            })

    # Test the constraint for bedrooms being greater than zero
    def test_03_bedrooms_constraint(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT1111',
                'description': 'Invalid Bedrooms',
                'postcode': '3030',
                'date_availability': fields.Date.today(),
                'bedrooms': 0,  # Invalid value
            })

    # Test if garden fields are properly initialized
    def test_04_garden_fields(self):
        property_id = self.property_02_record
        self.assertEqual(property_id.garden, False, "Garden field should be True.")
        self.assertEqual(property_id.garden_area, 50, "Garden area should be 50.")
        self.assertEqual(property_id.garden_orientation, 'north', "Garden orientation should be 'north'.")

    def test_05_default_values(self):
        property_id = self.property_02_record
        self.assertEqual(property_id.name, 'PRT1000', "Default name does not match the expected value.")
        self.assertEqual(property_id.expected_price, 1.0, "Default expected price should be 1.0.")
        self.assertIsNone(property_id.selling_price, "Selling price should be None by default.")

    def test_06_selling_price_constraint(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT2222',
                'description': 'Selling Price Issue',
                'postcode': '4040',
                'date_availability': fields.Date.today(),
                'expected_price': 50000,
                'selling_price': 40000,  # Selling price less than expected price
            })

    def test_07_boolean_field_behavior(self):
        property_id = self.env['property'].create({
            'name': 'PRT2000',
            'description': 'Test boolean fields',
            'postcode': '4040',
            'garage': True,
            'garden': True,
        })
        self.assertTrue(property_id.garage, "Garage should be True.")
        self.assertTrue(property_id.garden, "Garden should be True.")

    def test_08_invalid_data_type(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT3000',
                'description': 'Invalid Data Type',
                'postcode': '5050',
                'bedrooms': 'three',  # Invalid data type
            })

    def test_09_owner_relation(self):
        owner = self.env['owner'].create({'name': 'Test Owner'})
        property_id = self.env['property'].create({
            'name': 'PRT4000',
            'description': 'Relation Test',
            'postcode': '6060',
            'owner_id': owner.id,
        })
        self.assertEqual(property_id.owner_id.id, owner.id, "Owner ID should match the related record.")

    def test_10_multiple_records_creation(self):
        properties = self.env['property'].create([
            {'name': 'PRT5000', 'postcode': '7070'},
            {'name': 'PRT5001', 'postcode': '8080'},
        ])
        self.assertEqual(len(properties), 2, "Two records should be created.")

    def test_11_write_operation(self):
        property_id = self.property_02_record
        property_id.write({'description': 'Updated Description'})
        self.assertEqual(property_id.description, 'Updated Description', "Description should be updated.")

    def test_12_deletion(self):
        property_id = self.property_02_record
        property_id.unlink()
        properties = self.env['property'].search([('name', '=', 'PRT1000')])
        self.assertEqual(len(properties), 0, "Property should be deleted.")

    def test_13_garden_area_with_garden(self):
        with self.assertRaises(Exception):
            self.env['property'].create({
                'name': 'PRT7000',
                'postcode': '1111',
                'garden': False,
                'garden_area': 100,  # Invalid because garden is False
            })