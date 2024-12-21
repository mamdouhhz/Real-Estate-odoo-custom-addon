from odoo import models

# model types
# 1. "model", default model.
# 2. "Transient", does not need to store data.
# 3. "Abstract", does not create a table in database, you just inherit from it.

class ModelA(models.Model):
    _name = 'model.a'