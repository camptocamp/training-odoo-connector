# -*- coding: utf-8 -*-

import logging

from openerp import models, fields
from openerp.addons.connector.connector import ConnectorEnvironment, Binder
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.event import on_record_create, on_record_write
from openerp.addons.connector.unit.mapper import ExportMapper, mapping

from ..backend import odoo
from ..unit.backend_adapter import OdooBackendAdapter

_logger = logging.getLogger(__name__)


class PartnerBinding(models.Model):
    _name = 'odoo.res.partner'
    _inherit = 'external.binding'
    _inherits = {'res.partner': 'openerp_id'}
    _description = 'Odoo Partner Binding'

    openerp_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner',
                                 required=True,
                                 ondelete='cascade')
    backend_id = fields.Many2one(
        comodel_name='odoo.backend',
        string='Odoo Backend',
        required=True,
        ondelete='restrict',
    )
    external_id = fields.Integer(string='ID on the Odoo Backend')

    _sql_constraints = [
        ('backend_uniq', 'unique(backend_id, external_id)',
         'A binding already exists with the same external ID.'),
    ]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    odoo_bind_ids = fields.One2many(
        comodel_name='odoo.res.partner',
        inverse_name='openerp_id',
        string="Odoo Bindings",
    )


@on_record_create(model_names=['res.partner'])
@on_record_write(model_names=['res.partner'])
def on_change_export_partner(session, model_name, record_id, vals):
    record = session.env[model_name].browse(record_id)
    for binding in record.odoo_bind_ids:
        export_partner.delay(session, binding._name, binding.id)


@job
def export_partner(session, model_name, record_id):
    """ Exporting a partner """
    _logger.info('exporting %s with id %d', model_name, record_id)
    binding = session.env[model_name].browse(record_id)
    if not binding.exists():
        return

    backend = binding.backend_id
    connector_env = ConnectorEnvironment(
        backend,
        session,
        model_name
    )
    binder = connector_env.get_connector_unit(Binder)
    adapter = connector_env.get_connector_unit(OdooBackendAdapter)
    mapper = connector_env.get_connector_unit(ExportMapper)

    map_record = mapper.map_record(binding)
    external_id = binder.to_backend(binding)
    if external_id:
        adapter.write(external_id, map_record.values())
    else:
        external_id = adapter.create(map_record.values(for_create=True))
    binder.bind(external_id, binding)


@odoo
class PartnerAdapter(OdooBackendAdapter):
    _model_name = 'odoo.res.partner'
    _backend_model_name = 'res.partner'


@odoo
class PartnerBinder(Binder):
    _model_name = 'odoo.res.partner'


@odoo
class PartnerMapper(ExportMapper):
    _model_name = 'odoo.res.partner'

    direct = [
        ('name', 'name'),
        ('street', 'street'),
        ('street2', 'street2'),
        ('city', 'city'),
    ]

    @mapping
    def job(self, record):
        if not record.function:
            return {}
        return {'function': record.function.upper()}
