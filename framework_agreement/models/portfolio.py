# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Portfolio(models.Model):
    _name = 'framework.agreement.portfolio'
    _description = 'Agreement Portfolio'

    @api.multi
    def _company_get(self):
        company_id = self.env['res.company']._company_default_get(self._name)
        return self.env['res.company'].browse(company_id.id)

    @api.returns('self')
    @api.model
    def get_from_supplier(self, supplier):
        existing_portfolios = self.search([('supplier_id', '=', supplier.id)])
        if existing_portfolios:
            return existing_portfolios[0]
        else:
            return self.create({'supplier_id': supplier.id,
                                'name': supplier.name})

    name = fields.Char('Name', required=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=_company_get,
    )
    agreement_ids = fields.One2many(
        'framework.agreement', 'portfolio_id',
        'Agreements',
    )

    _sql_constraints = [('uniq_portfolio', 'unique(supplier_id, company_id)',
                'There can be only one portfolio per supplier and company.')]
