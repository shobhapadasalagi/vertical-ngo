# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Purchase Requisition Transport Document',
 'summary': 'Add Transport Documents to Purchase Requisitions',
 'version': '10.0.1.0.0',
 'author': 'Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.',
 'category': 'Purchase Management',
 'license': 'AGPL-3',
 'complexity': 'easy',
 'description': '''
Purchase Requisition Transport Document
=======================================
This module extends the purchase_transport_module allowing to add Transport
Documents to Purchase Requisitions as well. See the description of that module
for more information and demo data.
''',
 'depends': ['purchase_transport_document',
             'purchase_requisition',
             ],
 'data': ['view/purchase_requisition.xml',
          ],
 'installable': True,
 }
