# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common
from odoo import fields


class TestConsigneePurchaseOrder(common.TransactionCase):
    """ Test origin address is correctly set on picking
    """

    def setUp(self):
        super(TestConsigneePurchaseOrder, self).setUp()

        ref = self.env.ref
        self.part1 = ref('base.res_partner_1')
        self.part12 = ref('base.res_partner_12')

        PO = self.env['purchase.order']
        POL = self.env['purchase.order.line']

        po_vals = {
            'location_id': ref('stock.stock_location_stock').id,
            'partner_id': self.part12.id,
            }

        res = PO.onchange_partner_id(self.part12.id)
        po_vals.update(res['value'])

        self.po = PO.create(po_vals)

        pol_vals = {
            'order_id': self.po.id,
            'product_id': ref('product.product_product_33').id,
            'name': "[HEAD-USB] Headset USB",
            'product_qty': 24,
            'product_uom': ref('product.product_uom_unit').id,
            'date_planned': fields.Datetime.now(),
            'price_unit': 65,
            }
        POL.create(pol_vals)

    def test_create_picking_with_consignee(self):
        """Create a picking in from purchase order and check
        consignee is copied

        """

        self.po.consignee_id = self.part1.id
        self.po.signal_workflow('purchase_confirm')
        self.assertTrue(self.po.picking_ids)
        self.assertEquals(self.po.picking_ids.consignee_id,
                          self.po.consignee_id)

    def test_create_picking_without_consignee(self):
        """Create a picking in from purchase order
        remove origin address and check
        consignee is false on picking

        """
        self.po.signal_workflow('purchase_confirm')

        self.assertFalse(self.po.picking_ids.consignee_id.id)
