from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    # table name
    _name = 'property'

    # table columns with Logic Tier Validations [level 2].
    # Logic Tier Validations are applied on both presentation and logic tier.
    name = fields.Char(required=True, default='New') #default of required is false, we can say 1 for true or 0 for false
    description = fields.Char()
    postcode = fields.Char(required=1)
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(0, 5), default=1)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
         #db-val , #appears for user
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='south')
    owner_id = fields.Many2one('owner') # owner has many properties, property has 1 owner.
    tag_ids = fields.Many2many('tag') # only 'Many2one' is added to the database table. 'Many2many' makes a new table.

    # the best practice is to be named "state" and type is selection.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')

    # ------------------------------------------------------------------- Constraints ------------------------------------------------------------------------
    # Data Tier validations, strongest level of validation [level 1].
    _sql_constraints = [
        # constraint name, constraint, UI message
        ('unique_name', 'unique(name)', 'The name must be unique.'),
    ]

    # @api.constrains decorator
    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self): # self is the record set, maybe 1 or more records.
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('please add a valid number of bedrooms')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            print("inside draft method")

    def action_pending(self):
        for rec in self:
            rec.write({'state': 'pending'})
            print("inside pending method")

    def action_sold(self):
        for rec in self:
            rec.write({'state': 'sold'})
            print("inside sold method")

    # ------------------------------------------------------------------- CRUD Operations ------------------------------------------------------------------------
    # ----------------------------------------------------- They are inherited from the bas model "Model". -------------------------------------------------------
    # any function takes first argument as "self".
    # These are override demonstrations without actual implementation.

    # 1) Create.
    # Overriding the "Create" method of the super class Model, applies on all CRUD functions.
    @api.model_create_multi # or @api.model
    def _create(self, data_list):
        # models.Model._create(self, data_list)
        res = super(Property, self)._create(data_list)
        print("inside create method")
        return res

    # 2) Read.
    # Test it by just refreshing the tree view.
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        print("inside search method")
        return res

    # 3) Update.
    # Test it by updating an existing property.
    @api.model
    def _write(self, data_list):
        res = super(Property, self).write(data_list)
        print("inside write method")
        return res

    # # 4) Delete.
    # # mesh sha8ala bettala3 error.
    # # Test it by just refreshing the tree view.
    # @api.model
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------