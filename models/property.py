from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From") # حقل جديد
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True) # حقل للقراءة فقط
    bedrooms = fields.Integer(default=2)