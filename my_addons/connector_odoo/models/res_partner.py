# -*- coding: utf-8 -*-

import logging

import odoorpc

from openerp.addons.connector.queue.job import job
from openerp.addons.connector.event import on_record_create, on_record_write

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
    OdooBackendAdapter().create(values)


class OdooBackendAdapter(object):

    def __init__(self):
        super(OdooBackendAdapter, self).__init__()
        self.client = odoorpc.ODOO('localhost', port=9000)

    def _login(self):
        self.client.login('connector_odoo_target', 'admin', 'admin')

    def create(self, data):
        self._login()
        return self.client.env['res.partner'].create(data)

    def write(self, id, data):
        self._login()
        return self.client.env['res.partner'].browse(id).write(data)

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def read(self, id, **kwargs):
        raise NotImplementedError

    def search(self, filters, **kwargs):
        raise NotImplementedError
