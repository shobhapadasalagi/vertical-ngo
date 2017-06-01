# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Stock - Transport Addresses',
 'summary': 'Manage origin / destination / consignee addresses on pickings',
 'version': '10.0.1.0.0',
 'author': "Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.",
 'category': 'Warehouse',
 'license': 'AGPL-3',
 'complexity': 'expert',
 'website': "http://www.camptocamp.com",
 'depends': ['stock',
             ],
 'data': ['view/stock.xml',
          'view/procurement.xml',
          'view/res_partner.xml',
          ],
 'auto_install': False,
 'installable': True,
 }
