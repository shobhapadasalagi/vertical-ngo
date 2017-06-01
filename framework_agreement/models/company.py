# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Adds one_agreement_per_product field on company'

    one_agreement_per_product = fields.Boolean('One agreement per product',
                                               help='If checked you can have\
                                               only one framework agreement\
                                               per product at the same\
                                               time.')
