# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details

from odoo import models, api


class ConfirmGenerateAgreement(models.TransientModel):
    _name = 'confirm.generate.agreement'

    @api.multi
    def action(self):
        Model = self.env[self._context['active_model']]
        records = Model.browse(self._context['active_ids'])

        return records.agreement_selected()
