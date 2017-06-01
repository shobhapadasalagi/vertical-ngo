# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.one
    @api.depends('price_unit',
                 'price_subtotal',
                 'order_id.pricelist_id.currency_id',
                 'order_id.requisition_id.date_exchange_rate',
                 'order_id.requisition_id.pricelist_id.currency_id')
    def _compute_prices_in_company_currency(self):
        requisition = self.order_id.requisition_id
        if requisition and requisition.pricelist_id.currency_id:
            date = requisition.date_exchange_rate or fields.Date.today()
            # We take pricelist currency as currency should be related,
            # but due to odoo issue #4598 currency could mismatch
            from_curr = self.order_id.pricelist_id.currency_id
            from_curr = from_curr.with_context(date=date)
            to_curr = requisition.pricelist_id.currency_id
            self.price_unit_co = from_curr.compute(self.price_unit,
                                                   to_curr, round=False)
            self.price_subtotal_co = from_curr.compute(self.price_subtotal,
                                                       to_curr, round=False)

    price_unit_co = fields.Float(
        compute='_compute_prices_in_company_currency',
        string="Unit Price",
        digits=dp.get_precision('Account'),
        store=True,
        help="Unit Price in company currency.",
    )
    price_subtotal_co = fields.Float(
        compute='_compute_prices_in_company_currency',
        string="Subtotal",
        digits=dp.get_precision('Account'),
        store=True,
        help="Subtotal in company currency.",
    )
