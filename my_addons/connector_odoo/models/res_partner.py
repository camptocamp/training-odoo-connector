# -*- coding: utf-8 -*-

import logging

from openerp.addons.connector.connector import ConnectorEnvironment
from openerp.addons.connector.queue.job import job
from openerp.addons.connector.event import on_record_create, on_record_write

from ..backend import odoo
from ..unit.backend_adapter import OdooBackendAdapter

_logger = logging.getLogger(__name__)


@on_record_create(model_names=['res.partner'])
@on_record_write(model_names=['res.partner'])
def on_change_export_partner(session, model_name, record_id, vals):
    export_partner.delay(session, model_name, record_id)


@job
def export_partner(session, model_name, record_id):
    """ Exporting a partner """
    _logger.info('exporting %s with id %d', model_name, record_id)
    record = session.env[model_name].browse(record_id)
    if not record.exists():
        return
    values = {
        'name': record.name,
        'street': record.street,
        'street2': record.street2,
    }
    backend_records = session.env['odoo.backend'].search([])
    for backend in backend_records:
        connector_env = ConnectorEnvironment(
            backend,
            session,
            model_name
        )
        adapter = connector_env.get_connector_unit(OdooBackendAdapter)
        adapter.create(values)


@odoo
class PartnerAdapter(OdooBackendAdapter):
    _model_name = 'res.partner'
    _backend_model_name = 'res.partner'
