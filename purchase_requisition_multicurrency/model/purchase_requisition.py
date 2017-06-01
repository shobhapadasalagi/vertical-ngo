# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.tools import SUPERUSER_ID


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    date_exchange_rate = fields.Date('Exchange rate reference date',
        help="Defines Exchange rate date of Unit price and subtotal \
             If not set, takes todays exchange rate.")
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist',
        required=True,
        help="Pricelist that represent the currency for current logistic \
             request.")
    currency_id = fields.Many2one(
        related='pricelist_id.currency_id',
        comodel_name='res.currency',
        string='Currency',
    )

#    @api.model
#    def _auto_init(self):
#        """Fill in the required field with default values.
#        This is similar to the solution used in mail_alias.py in the core.
#        The installation of the module will succeed with no errors, and the
#        column will be required immediately (the previous solution made it
#        required only on the first module update after installation).
#        """
#        # create the column non required
#        self._columns['pricelist_id'].required = False
#        super(PurchaseRequisition, self)._auto_init()
#
#        default_pricelist_id = self.env['product.pricelist'].search(
#             SUPERUSER_ID, [('type', '=', 'purchase')], limit=1,
#        )[0]
#
#    # do not use the ORM, because it would try to recompute fields that are
#    # not fully initialized
#        cr.execute('''
#                   UPDATE purchase_requisition
#                   SET pricelist_id = %s
#                   WHERE pricelist_id IS NULL;
#                   ''', (default_pricelist_id,))
#
#        # make the column required again
#        self._columns['pricelist_id'].required = True
#        super(PurchaseRequisition, self)._auto_init()
