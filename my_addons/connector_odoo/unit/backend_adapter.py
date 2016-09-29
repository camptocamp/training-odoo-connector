# -*- coding: utf-8 -*-

import odoorpc
from openerp.addons.connector.unit.backend_adapter import CRUDAdapter


class OdooBackendAdapter(CRUDAdapter):

    _backend_model = None

    def __init__(self, connector_env):
        super(OdooBackendAdapter, self).__init__(connector_env)
        backend = self.connector_env.backend_record
        self.client = odoorpc.ODOO(backend.host, port=backend.port)

    def _login(self):
        backend = self.connector_env.backend_record
        self.client.login(backend.database, backend.username, backend.password)

    def create(self, data):
        self._login()
        return self.client.env[self._backend_model_name].create(data)

    def write(self, id, data):
        self._login()
        model = self.client.env[self._backend_model_name]
        return model.browse(id).write(data)

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def read(self, id, **kwargs):
        raise NotImplementedError

    def search(self, filters, **kwargs):
        raise NotImplementedError
