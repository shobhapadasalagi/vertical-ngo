# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class TestConsigneeSaleOrder(common.TransactionCase):
    """ Test origin address is correctly set on picking
    """

    def setUp(self):
        super(TestConsigneeSaleOrder, self).setUp()
        ref = self.env.ref

        part1 = ref('base.res_partner_1')
        part12 = ref('base.res_partner_12')
        self.env['res.partner'].create(
            {'name': 'part12 delivery',
             'type': 'delivery',
             'parent_id': part12.id})
        SO = self.env['sale.order']
        SOL = self.env['sale.order.line']

        so_vals = {
            'partner_id': part12.id,
            'consignee_id': part1.id,
            }

        res = SO.onchange_partner_id(part12.id)
        so_vals.update(res['value'])

        self.so = SO.create(so_vals)

        # sale exceptions, if installed, is irrelevant here. If it isn't this
        # is no-op
        self.so.ignore_exceptions = True

        sol_vals = {
            'order_id': self.so.id,
            'product_id': ref('product.product_product_33').id,
            'name': "[HEAD-USB] Headset USB",
            'product_uom_qty': 24,
            'product_uom': ref('product.product_uom_unit').id,
            'price_unit': 65,
            }
        SOL.create(sol_vals)

    def test_create_picking_from_so(self):
        """Create a picking in from purchase order and check
        consignee is copied

        """
        self.assertEquals(self.so.partner_shipping_id.parent_id,
                          self.so.partner_id)
        self.so.signal_workflow('order_confirm')
        self.assertEquals(self.so.picking_ids.consignee_id,
                          self.so.consignee_id)
        self.assertEquals(self.so.picking_ids.origin_address_id,
                          self.so.company_id.partner_id)
        self.assertEquals(self.so.picking_ids.delivery_address_id,
                          self.so.partner_shipping_id)
        self.assertEquals(self.so.picking_ids.partner_id,
                          self.so.partner_id)
