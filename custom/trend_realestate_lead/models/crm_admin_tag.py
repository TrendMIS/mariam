from odoo import models, fields


class CrmAdminTag(models.Model):
    _name = 'crm.admin.tag'

    name = fields.Char()
