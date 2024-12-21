from odoo import models

class ModelD(models.Model):
    _name = 'model.d'
    _log_access = False # doe
    # s not create ["create_uid", "write_uid", "create_date", "write_date"] columns.