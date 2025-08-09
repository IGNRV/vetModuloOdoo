from odoo import models, fields, api

class Surgery(models.Model):
    _name = "animal.surgery"
    _description = "Animal surgeries table"

    name = fields.Char(string="Cirugía", required=True)
    observations = fields.Text(string="Observaciones")
