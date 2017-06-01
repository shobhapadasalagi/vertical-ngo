# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Purchase - Transport Addresses',
 'summary': 'Manage origin / destination / consignee addresses on purchases',
 'version': '10.0.1.0.0',
 'author': "Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.",
 'category': 'Warehouse',
 'license': 'AGPL-3',
 'complexity': 'expert',
 'website': "http://www.camptocamp.com",
 'depends': ['purchase',
             'stock_transport_multi_address',
             'sale_transport_multi_address',
             ],
 'data': ['view/purchase.xml',
          ],
 'auto_install': False,
 'installable': True,
 }
