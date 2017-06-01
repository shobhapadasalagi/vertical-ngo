# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = 'Add relation to framework agreement'

    framework_agreement_ids = fields.One2many(
        comodel_name='framework.agreement',
        inverse_name='product_id',
        string='Framework Agreements (LTA)',
        copy=False,
    )
