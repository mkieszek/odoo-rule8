# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Payment Przelewy24',
    'version': '0.1',
    'category': 'Payment Acquirer: Przelwy24 Implementation',
    'description': """Przelwy24 Payment Acquirer""",
    'author': 'Via IT Solution',
    'website': 'http://www.viait.pl ',
    'depends': ['payment'],
    'data': [
             'data/przelewy24_data.xml',
             ],
    'demo': [],
    'test':[],
    'installable': True,
    'images': [],
    'update_xml' : [
                    'view/przelewy24_acquirer.xml',
                    'view/przelewy24_view.xml',
                    ],
    'sequence': 1001,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
# -*- coding: utf-8 -*-