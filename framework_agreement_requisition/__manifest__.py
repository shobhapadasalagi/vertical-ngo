# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details

{'name': 'Framework Agreement Negociation in the Tender',
 'version': '10.0.1.0.0',
 'license': 'AGPL-3',
 'author': "Camptocamp,Odoo Community Association (OCA), \
         Serpent Consulting Services Pvt. Ltd.",
 'maintainer': 'Camptocamp',
 'category': 'NGO',
 'complexity': 'normal',
 'depends': ['purchase_requisition',
             'purchase_requisition_bid_selection',
             'ngo_purchase_requisition',
             'framework_agreement'],
 'website': 'http://www.camptocamp.com',
 'data': [
          'view/purchase_requisition.xml',
          'view/purchase_order.xml',
          'wizard/confirm_generate_agreement.xml'
          ],
 'installable': True,
 'auto_install': False,
 'application': False,
}
