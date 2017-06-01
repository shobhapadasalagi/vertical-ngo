# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo import models, fields, api


# Using new API seem to have side effect on
# other official addons
class ProductPricelist(models.Model):
    _inherit = "product.pricelist"
    _description = "Add framework agreement behavior on pricelist"

    @api.multi
    def _plist_is_agreement(self, pricelist_id):
        """
        Check that a price list can be subject to agreement.
        :param pricelist_id: the price list to be validated
        :returns: a boolean (True if agreement is applicable)
        """
        p_list = self.browse(pricelist_id)
        return p_list.type == 'purchase'

    @api.multi
    def price_get(self, prod_id, qty, partner=None, context=None):
        """Override of price retrieval function in order to support framework
        agreement.
        If it is a supplier price list, agreement will be taken in account
        and use the price of the agreement if required.
        If there is not enough available qty on agreement,
        standard price will be used.
        This is maybe a faulty design and we should use on_change override
        """
        if self._context is None:
            context = {}
        agreement_obj = self.env['framework.agreement']
        res = super(ProductPricelist, self).price_get(
            prod_id, qty, partner=partner, context=context)
        if not partner:
            return res
        for pricelist_id in res:
            if (pricelist_id == 'item_id' or not
                    self._plist_is_agreement(
                                             pricelist_id, context=context)):
                continue
            now = datetime.strptime(fields.date.today(),
                                    DEFAULT_SERVER_DATE_FORMAT)
            date = self._context.get('date') or self._context.get
            ('date_order') or now
            prod = self.pool['product.product'].browse(prod_id,
                                                       context=context)
            agreement = agreement_obj.get_product_agreement(
                prod.product_tmpl_id.id, partner, date, qty=qty,
                context=context
            )
            if agreement is not None:
                currency = agreement_obj._get_currency(
                    partner, pricelist_id,
                    context=context
                )
                res[pricelist_id] = agreement.get_price(qty,
                                            currency=currency)
        return res
