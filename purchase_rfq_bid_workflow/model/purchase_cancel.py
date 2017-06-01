# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class PurchaseCancelReason(models.Model):
    _name = "purchase.cancel_reason"

    name = fields.Char('Reason', size=64, required=True, translate=True)
    type = fields.Selection(
        [('rfq', 'RFQ/Bid'),
         ('purchase', 'Purchase Order')],
        'Type', required=True,
    )
    nounlink = fields.Boolean('No unlink')

    @api.one
    def unlink(self):
        """ Prevent to unlink records that are used in the code
        """
        if self.nounlink:
            return True
        else:
            return super(PurchaseCancelReason, self).unlink()
