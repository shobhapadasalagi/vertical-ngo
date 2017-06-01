# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{"name": "Purchase Transport Document",
 "summary": "Add a new Transport Document object in the Purchase Order",
 "version": "10.0.0.1.0",
 "author": "Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.",
 "category": "Purchase Management",
 "license": "AGPL-3",
 'complexity': "easy",
 "depends": ["purchase",
             ],
 "data": ["view/purchase_order.xml",
          "view/transport_document.xml",
          "security/ir.model.access.csv",
          "data/transport_document.xml",
          ],
 "installable": True,
 }
