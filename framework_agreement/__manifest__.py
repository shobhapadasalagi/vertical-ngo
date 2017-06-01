# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

{'name': 'Framework Agreement',
 'summary': 'Long Term Agreement (or Framework Agreement) for purchases',
 'version': '10.0.1.0.0',
 'license': 'AGPL-3',
 'author': "Camptocamp,Odoo Community Association (OCA),\
        Serpent Consulting Services Pvt. Ltd.",
 'category': 'Purchase Management',
 'complexity': 'normal',
 'depends': ['stock', 'procurement', 'purchase', 'web_context_tunnel'],
 'website': 'http://www.camptocamp.com',
 'data': [
          'data.xml',
          'view/product_view.xml',
          'view/framework_agreement_view.xml',
          'view/portfolio.xml',
          'view/purchase_view.xml',
          'view/company_view.xml',
          'security/multicompany.xml',
          'security/groups.xml',
          'security/ir.model.access.csv'
],
 'installable': True,
 'auto_install': False,
 'application': False,
}
