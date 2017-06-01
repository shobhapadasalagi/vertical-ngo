# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = "Add fields related to consignee \
             A consignee is a special kind of partner \
            that is in charge of receiving goods."

    is_consignee = fields.Boolean('Consignee')
