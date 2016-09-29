# -*- coding: utf-8 -*-

import logging

from openerp.addons.connector.queue.job import job
from openerp.addons.connector.event import on_record_create, on_record_write

_logger = logging.getLogger(__name__)


@on_record_create(model_names=['res.partner'])
@on_record_write(model_names=['res.partner'])
def on_change_export_partner(session, model_name, record_id, vals):
    export_partner(session, model_name, record_id)


@job
def export_partner(session, model_name, record_id):
    """ Exporting a partner """
    _logger.info('exporting %s with id %d', model_name, record_id)
