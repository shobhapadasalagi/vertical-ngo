# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class TransportDocument(models.Model):
    _name = "transport.document"

    name = fields.Char('Name', translate=True)
