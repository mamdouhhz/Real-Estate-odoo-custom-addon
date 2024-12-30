from odoo import models, fields

class Tags(models.Model):
    _name = 'tag'

    name = fields.Char(required=True)