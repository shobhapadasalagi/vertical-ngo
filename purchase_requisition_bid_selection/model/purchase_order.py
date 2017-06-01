# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PurchaseOrderClassic(models.Model):
    _inherit = "purchase.order"

    tender_bid_receipt_mode = fields.Selection([('open', 'Open'),
                                                ('sealed', 'Sealed')],
            related='requisition_id.bid_receipt_mode',
            string='Bid Receipt Mode')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Keep requisition_id when copying a PO or a bid
    requisition_id = fields.Many2one(copy=True)
    bid_partial = fields.Boolean('Bid partially selected', readonly=True,
        help="True if the bid has been partially selected")
    keep_in_draft = fields.Boolean('Prevent validation of purchase order.',
        help="Technical field used to prevent the PO that is automatically\
        generated from a Tender to be validated. It is checked on the \
        workflow transition.")
    delivery_remark = fields.Text('Delivery Remarks')
    terms_of_payment = fields.Char()
    country_of_origin = fields.Many2one('res.country')
    volume_estimated = fields.Float('Volume estimated (m3)')
    weight_estimated = fields.Float('Weight estimated (kg)')
    meets_specifications = fields.Boolean()
    bid_eligible = fields.Boolean()
    bid_internal_remark = fields.Text('Internal remarks')

    @api.model
    def _prepare_purchase_order(self, requisition, supplier):
        values = super(PurchaseOrder, self
                       )._prepare_purchase_order(requisition, supplier)
        values.update({
            'bid_validity': requisition.req_validity,
            'payment_term_id': requisition.req_payment_term_id,
            'incoterm_id': requisition.req_incoterm_id,
            'incoterm_address': requisition.req_incoterm_address,
            'transport_mode_id': requisition.req_transport_mode_id,
        })
        if requisition.pricelist_id:
            values.update({'pricelist_id': requisition.pricelist_id.id})
        return values

    @api.one
    def copy(self, default=None):
        """ Need to set origin after copy because original copy clears origin
        """
        if default is None:
            default = {}
        initial_origin = default.get('origin')
        newpo = super(PurchaseOrder, self).copy(default=default)

        if initial_origin and 'requisition_id' in default:
            newpo.sudo().origin == initial_origin
        return newpo


class PurchaseOrderLineClassic(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def read_group(self, *args, **kwargs):
        """Do not aggregate price and qty. We need to do it this way as there
        is no group_operator that can be set to prevent aggregating float"""

        result = super(PurchaseOrderLineClassic, self).read_group(*args,
                                                                  **kwargs)

        for res in result:
            if 'price_unit' in res:
                del res['price_unit']
            if 'product_qty' in res:
                del res['product_qty']
            if 'lead_time' in res:
                del res['lead_time']
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    remark = fields.Text('Remarks / Conditions')
    requisition_line_id = fields.Many2one(
        'purchase.requisition.line',
        'Call for Bid Line',
        readonly=True,
    )
    country_of_origin = fields.Many2one(
        'res.country',
        related='order_id.country_of_origin',
    )
    incoterm_id = fields.Many2one(
        'stock.incoterms', string='Incoterm',
        related='order_id.incoterm_id', store=True,
    )
    incoterm_address = fields.Char(
        'Incoterms place',
        related='order_id.incoterm_address',
    )
    terms_of_payment = fields.Char(related='order_id.terms_of_payment')
    meets_specifications = fields.Boolean(
        related='order_id.meets_specifications', store=True,
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
        related='order_id.payment_term_id',
    )
    bid_eligible = fields.Boolean(
        related='order_id.bid_eligible',
        store=True,
    )
