# -*- coding: utf-8 -*-
import pdb
import md5

from openerp import http, SUPERUSER_ID
from openerp.http import request


class Przelewy24Controller(http.Controller):
    return_url_ok = '/payment/przelewy24/confirm'
    return_url_error = '/payment/przelewy24/error'
    
    def przelewy24_confirm(self, post):
        #pdb.set_trace()
        #self.pool.get('payment.acquirer')._get_przelewy24_urls(cr, uid, acquirer.environment, context=context)['przelewy24_rest_url']
        return True

    @http.route('/payment/przelewy24/confirm', type='http', auth="none")
    def przelewy24_ok(self, **post):
        """Obsługa prawidłowo przeprowadzonej transakcji"""

        #parametry otrzymane jako potwierdzenie
        get_value = ['p24_session_id','p24_order_id','p24_kwota','p24_karta','p24_order_id_full','p24_crc']
        val = '<h3>Przekazywane parametry</h2>'
            
        for value in get_value:
            if value in post:
                val += '<div>'+value+': '+post[value]+'</div>'
            else:
                val += '<div>'+value+': BRAK''</div>'
        #pdb.set_trace()
        if 'p24_session_id' in post and 'p24_kwota' in post and 'p24_crc' in post:
            crc = md5.new("%s|%s|%s|%s"\
                          %(post['p24_session_id'],'9999',post['p24_kwota'],'a123b456c789d012')).hexdigest()
            if crc == post['p24_crc']:
                val += '<div style="color:green">zgodność sumy kontrolnej</div>'.decode('utf-8')
                #potwierdzenie otrzymania prawidłowej odpowiedzi
                self.przelewy24_confirm(post)
            else:
                val += '<div style="color:red">niezgodność sumy kontrolnej</div>'.decode('utf-8')
        return val

    @http.route('/payment/przelewy24/error', type='http', auth="none")
    def przelewy24_error(self, **post):
        """Obsługa błędu transakcji"""
        #pdb.set_trace()
        return '<h3>Test Błędu</h3>'