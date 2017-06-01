# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Purchase Requisition - Transport Addresses',
 'summary': 'Manage origin / destination / consignee addresses '
            'on purchase requisitions',
 'version': '10.0.1.0.0',
 'author': "Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.",
 'category': 'Warehouse',
 'license': 'AGPL-3',
 'complexity': 'expert',
 'website': "http://www.camptocamp.com",
 'depends': ['purchase_requisition',
             'purchase_transport_multi_address'
             ],
 'demo': [],
 'data': ['view/purchase_requisition.xml',
          ],
 'auto_install': True,
 'installable': True,
 }
