from odoo import fields, models

class ResPartnerDetails(models.Model):
    _name = "res.partner.details"
    _description = "Thông tin môi giới"

    name = fields.Char(string="Tên")
    age = fields.Integer(string="Tuổi")