# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Housing Cooperative',
    'summary': 'Manage your housing cooperative',
    'author': 'Coop IT Easy SCRL',
    'website': 'https://coopiteasy.be',
    'category': 'Uncategorized',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'contacts',
        'contract',
        'contract_sale',
        'partner_contact_birthdate',
        'partner_contact_gender',
        'partner_firstname',
        'partner_household',
        # 'partner_secondary_address',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/building.xml',
        'views/cluster.xml',
        'views/housing.xml',
        'views/lease.xml',
        'views/permit.xml',
        'views/plan.xml',
        'views/res_partner.xml',
        'views/room.xml',
        'views/cellar.xml',
        'views/studies.xml',
        'views/menu.xml',
        'demo/demo.xml',  # fixme
        'data/data.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
}