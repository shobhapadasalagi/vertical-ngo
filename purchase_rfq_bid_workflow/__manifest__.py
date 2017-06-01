# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Purchase RFQ Bid workflow',
 'summary': 'Improve the purchase workflow to manage RFQ, Bids, and Orders',
# 'post_init_hook': 'fix_inconsistent_initial_types',
 'version': '10.0.0.3.0',
 'author': 'Camptocamp,Odoo Community Association (OCA),\
         Serpent Consulting Services Pvt. Ltd.',
 'category': 'Purchase Management',
 'license': 'AGPL-3',
 'complexity': 'normal',
 'description': '''
This module improves the standard Purchase module.
==================================================
In standard, RFQs, Bids and PO are all the same object.  The purchase workflow
has been improved with a new 'Draft PO' state to clearly differentiate the
RFQ->Bid workflow and the PO workflow. A type field has also been added to
identify if a document is of type 'rfq' or 'purchase'. This is particularly
useful for canceled state and for datawarehouse.

The 'Requests for Quotation' menu entry shows only documents of type 'rfq' and
the new documents are created in state 'Draft RFQ'. Those documents have lines
with a price, by default, set to 0; it will have to be encoded when the bid is
received. The state 'Bid Received' has been renamed 'Bid Encoded'. This clearly
indicates that the price has been filled in. The bid received date will be
requested when moving to that state.

The 'Purchase Orders' menu entry shows only documents of type 'purchase' and
the new documents are created in state 'Draft PO'.

The logged messages have been improved to notify users at the state changes and
with the right naming.


In the scope of international transactions, some fields have been added:
 - Consignee: the person to whom the shipment is to be delivered
 - Incoterms Place: the standard incoterms field specifies the incoterms rule
   that applies. This field allows to name the place where the goods will be
   available

TODO: describe onchange picking type.

Note: for running the tests, the python package nose is required. It is not
listed as an external dependency because it is not needed in production.
''',
 'depends': ['purchase',
             'web_context_tunnel',
             ],
    'data': [
             'view/purchase_order.xml',
             'view/purchase_cancel.xml',
             'data/purchase_order.xml',
             'wizard/modal.xml',
             'wizard/action_cancel_reason.xml',
             'security/ir.model.access.csv',
             ],
    'auto_install': False,
    'installable': True,
 }
