{'name': 'Connector Odoo Training',
 'author': '',
 'version': '1.0',
 'category': 'Tools',
 'description': """,
Connector Odoo Training
=======================

Didactic addon used in Odoo Connector trainings.

 """,
 'depends': ['connector'],
 'external_dependencies': {
     'python': ['odoorpc'],
 },
 'data': [
     'views/odoo_backend_views.xml',
     'views/res_partner_views.xml',
  ],
 'images': [],
 'demo': [],
 'application': True,
 }
