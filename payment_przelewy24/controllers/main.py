# -*- coding: utf-8 -*-
import pdb

from openerp import http, SUPERUSER_ID
from openerp.http import request


class Przelewy24Controller(http.Controller):
    return_url_ok = '/payment/przelewy24/confirm'
    return_url_error = '/payment/przelewy24/error'

    @http.route('/payment/przelewy24/confirm', type='http', auth="none")
    def przelewy24_ok(self, **post):
        #pdb.set_trace()
        get_value = ['p24_session_id','p24_order_id','p24_kwota','p24_karta','p24_order_id_full','p24_crc']
        val = '<h3>Przekazywane parametry</h2>'
            
        for value in get_value:
            if value in post:
                val += '<div>'+value+': '+post[value]+'</div>'
            else:
                val += '<div>'+value+': BRAK''</div>'
        return val

    @http.route('/payment/przelewy24/error', type='http', auth="none")
    def przelewy24_error(self, **post):
        #pdb.set_trace()
        return '<h3>Test Błędu</h3>'