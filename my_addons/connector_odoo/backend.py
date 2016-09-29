# -*- coding: utf-8 -*-

import openerp.addons.connector.backend as backend


odoo = backend.Backend('odoo')
""" Generic Odoo Backend """

odoo_8_0 = backend.Backend(parent=odoo, version='8.0')
""" Odoo Backend for version 8.0 """

odoo_9_0 = backend.Backend(parent=odoo, version='9.0')
""" Odoo Backend for version 9.0 """

odoo_10_0 = backend.Backend(parent=odoo, version='10.0')
""" Odoo Backend for version 10.0 """
