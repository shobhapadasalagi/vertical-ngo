# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing detail

def migrate(cr, installed_version):
    """Add missing portfolios to agreements, create them if necessary."""
    cr.execute('SELECT a.id, a.supplier_id, p.name '
               'FROM framework_agreement a '
               'JOIN res_partner p '
               'ON a.supplier_id = p.id '
               'WHERE portfolio_id is null;')

    for agreement_id, supplier_id, supplier_name in cr.fetchall():
        cr.execute(
            'SELECT id '
            'FROM framework_agreement_portfolio '
            'WHERE supplier_id = %s;',
            (supplier_id,),
        )
        portfolios = cr.fetchone()
        if portfolios:
            new_portfolio = portfolios[0]
        else:
            cr.execute('INSERT INTO framework_agreement_portfolio '
                       '(name, supplier_id) '
                       'VALUES (%s, %s) '
                       'RETURNING id; ',
                       (supplier_name, supplier_id))
            new_portfolio = cr.fetchone()[0]

        cr.execute('UPDATE framework_agreement '
                   'SET portfolio_id = %s '
                   'WHERE id = %s',
                   (new_portfolio, agreement_id),
                   )
