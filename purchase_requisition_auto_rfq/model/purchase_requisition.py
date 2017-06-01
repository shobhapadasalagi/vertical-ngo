# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details

from collections import defaultdict

from odoo import models, api
from odoo.tools.translate import _


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.multi
    def auto_rfq_from_suppliers(self):
        """create purchase orders from registered suppliers for products in the
        requisition.

        The created PO for each supplier will only concern the products for
        which an existing product.supplierinfo record exist for that product.
        """
        po_obj = self.env['purchase.order']
        po_line_obj = self.env['purchase.order.line']
        seller_products = defaultdict(set)
        for requisition in self:
            products_without_supplier = []
            for line in requisition.line_ids:
                sellers = line.product_id.product_tmpl_id.seller_ids
                if not sellers:
                    products_without_supplier.append(line.product_id)
                for seller in sellers:
                    seller_products[seller.name.id].add(line.product_id.id)
            if products_without_supplier:
                body = _(u'<p><b>RFQ generation</b></p>'
                         '<p>The following products have no '
                         'registered suppliers and are not included in the '
                         'generated RFQs:<ul>%s</ul></p>')
                body %= ''.join(u'<li>%s</li>' % product.name
                                for product in products_without_supplier)
                self.message_post(body=body,
                                  subject=_(u'RFQ Generation'))
        lines_to_remove = po_line_obj.browse()
        for seller_id, sold_products in seller_products.iteritems():
            po_info = self.make_purchase_order(seller_id)
            # make_purchase_order creates po lines for all the products in the
            # requisition. We need to unlink all the created lines for which
            # the supplier is not an official supplier for the product.
            po_ids = po_info.values()
            for purchase in po_obj.browse(po_ids):
                for line in purchase.order_line:
                    if line.product_id.id not in sold_products:
                        lines_to_remove |= line
        lines_to_remove.unlink()
        return True
