from odoo import models, fields

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Char()

    # field 'property_ids' not stored in database.
    # One2many, Many2Many: _ids
    # Many2one: _id
    # 'owner_id': is the foreign key in table 'property'.
    property_ids = fields.One2many('property', 'owner_id')
