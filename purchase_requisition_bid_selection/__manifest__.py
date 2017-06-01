# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Purchase Requisition Bid Selection',
 'version': '10.0.1.0.0',
 'author': 'Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.',
 'license': 'AGPL-3',
 'category': 'Purchase Management',
 'complexity': 'normal',
 'depends': ['purchase_requisition', 'stock',  # For incoterms
             'purchase_rfq_bid_workflow',
             'purchase_requisition_multicurrency',
             ],
 'data': [
          'wizard/modal.xml',
          'wizard/purchase_requisition_partner_view.xml',
          'wizard/update_bid_internal_remark.xml',
          'wizard/update_remark.xml',
          'view/purchase_requisition.xml',
          'view/purchase_order.xml',
          'view/report_purchaserequisition.xml',
          'report.xml',
          ],
 'auto_install': False,
 'installable': True,
 }
