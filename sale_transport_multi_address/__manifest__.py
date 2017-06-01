# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Sale - Transport Addresses',
 'summary': 'Manage origin / destination / consignee addresses on sales',
 'version': '8.0.1.0.0',
 'author': "Camptocamp,Odoo Community Association (OCA)",
 'category': 'Warehouse',
 'license': 'AGPL-3',
 'complexity': 'expert',
 'website': "http://www.camptocamp.com",
 'depends': ['sale_stock',
             'stock_transport_multi_address',
             ],
 'demo': ['demo/sale.xml',
          ],
 'data': [
          'view/sale.xml',
          'view/report_saleorder.xml',
          ],
 'auto_install': False,
 'installable': True,
 }
