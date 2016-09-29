# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OdooBackend(models.Model):
    _name = 'odoo.backend'
    _description = 'Odoo Backend'
    _inherit = 'connector.backend'

    _backend_type = 'odoo'

    version = fields.Selection(selection='select_versions', required=True)

    @api.model
    def select_versions(self):
        return [('8.0', '8.0'), ('9.0', '9.0'), ('10.0', '10.0')]

    host = fields.Char(required=True, default='localhost')
    port = fields.Integer(required=True, default=8069)
    username = fields.Char(required=True)
    password = fields.Char(required=True)
    database = fields.Char(required=True)
