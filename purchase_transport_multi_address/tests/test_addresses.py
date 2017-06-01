# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common
from odoo import fields


class TestAddresses(common.TransactionCase):

    def setUp(self):
        super(TestAddresses, self).setUp()

        ref = self.env.ref
        self.part1 = ref('base.res_partner_1')
        self.part12 = ref('base.res_partner_12')
        PO = self.env['purchase.order']
        POL = self.env['purchase.order.line']

        po_vals = {
            'partner_id': self.part1.id,
            'location_id': ref('stock.stock_location_stock').id
        }

        res = PO.onchange_partner_id(self.part1.id)
        po_vals.update(res['value'])
        self.po = PO.create(po_vals)

        POL.create({
            'order_id': self.po.id,
            'product_id': ref('product.product_product_33').id,
            'name': "[HEAD-USB] Headset USB",
            'product_qty': 24,
            'product_uom': ref('product.product_uom_unit').id,
            'date_planned': fields.Datetime.now(),
            'price_unit': 65,
        })

    def test_propagate_empty_address_to_picking(self):
        self.po.signal_workflow('purchase_confirm')
        self.assertFalse(self.po.picking_ids.delivery_address_id.id)

    def test_propagate_supplier_and_chosen_address_to_picking(self):
        self.po.dest_address_id = self.part12.id
        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(self.po.picking_ids.delivery_address_id,
                          self.po.dest_address_id)
        self.assertEquals(self.po.picking_ids.partner_id,
                          self.po.partner_id)

    def test_create_picking_with_default_origin(self):
        """Create a picking in from purchase order and check
        origin address is copied

        """

        self.po.signal_workflow('purchase_confirm')
        self.assertTrue(self.po.origin_address_id)
        self.assertEquals(self.po.picking_ids.origin_address_id,
                          self.po.origin_address_id)

    def test_create_picking_without_origin(self):
        """Create a picking in from purchase order
        remove origin address and check
        origin address is false on picking

        """

        self.po.origin_address_id = False
        self.po.signal_workflow('purchase_confirm')
        self.assertFalse(self.po.picking_ids.origin_address_id.id)

    def test_create_picking_with_other_origin(self):
        """Create a picking in from purchase order and check
        origin address is copied and is the same as on the purchase
        order

        """

        self.po.origin_address_id = self.part12.id
        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(self.po.picking_ids.origin_address_id,
                          self.po.origin_address_id)
