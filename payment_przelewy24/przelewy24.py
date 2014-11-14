# -*- coding: utf-'8' "-*-"
from openerp.osv import osv, fields
from openerp import SUPERUSER_ID
from openerp.addons.payment_przelewy24.controllers.main import Przelewy24Controller
import urlparse
import md5
import cherrypy
import base64
try:
    import simplejson as json
except ImportError:
    import json
import pdb


class AcquirerPaypal(osv.Model):
    _inherit = 'payment.acquirer'
    
    def _get_przelewy24_urls(self, cr, uid, environment, context=None):
        """ Paypal URLS """
        if environment == 'prod':
            return {
                'przelewy24_form_url': 'https://secure.przelewy24.pl/index.php',
                'przelewy24_rest_url': 'https://secure.przelewy24.pl/transakcja.php',
            }
        else:
            return {
                'przelewy24_form_url': 'https://sandbox.przelewy24.pl/index.php',
                'przelewy24_rest_url': 'https://sandbox.przelewy24.pl/transakcja.php',
            }
    
    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerPaypal, self)._get_providers(cr, uid, context=context)
        providers.append(['przelewy24', 'Przelewy24'])
        return providers
    
    _columns = {
        'przelewy24_merchant_id': fields.char('Przelewy24 Merchant ID'),
        'przelewy24_crc': fields.char('Klucz CRC'),
    }
    
    def przelewy24_form_generate_values(self, cr, uid, id, partner_values, tx_values, context=None):
        base_url = self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)
        #pdb.set_trace()
        
        #ID sesji
        session = 'test'
        
        przelewy24_tx_values = dict(tx_values)
        przelewy24_tx_values.update({
            'item_name': tx_values['reference'],
            'amount': int(tx_values['amount']*100),
            'currency_code': tx_values['currency'] and tx_values['currency'].name or '',
            'address1': partner_values['address'],
            'city': partner_values['city'],
            'country': partner_values['country'] and partner_values['country'].name or '',
            'state': partner_values['state'] and partner_values['state'].name or '',
            'email': partner_values['email'],
            'zip': partner_values['zip'],
            'client_name': tx_values['partner'].name,
            'description': tx_values['reference']+', partner - ID:'+str(tx_values['partner'].id)+' Name:'+tx_values['partner'].name,
            'language': (partner_values['lang'][0]+partner_values['lang'][1]) or False,
            'merchant_id': acquirer.przelewy24_merchant_id,
            'crc': md5.new("%s|%s|%s|%s"%(session,acquirer.przelewy24_merchant_id,str(int(tx_values['amount']*100)),acquirer.przelewy24_crc)).hexdigest(),
            'session_id': session,
            'return_url_ok': '%s' % urlparse.urljoin(base_url, Przelewy24Controller.return_url_ok),
            'return_url_error': '%s' % urlparse.urljoin(base_url, Przelewy24Controller.return_url_error),
        })
        #pdb.set_trace()
        if acquirer.fees_active:
            przelewy24_tx_values['handling'] = '%.2f' % przelewy24_tx_values.pop('fees', 0.0)
        if przelewy24_tx_values.get('return_url'):
            przelewy24_tx_values['custom'] = json.dumps({'return_url': '%s' % przelewy24_tx_values.pop('return_url')})
        return partner_values, przelewy24_tx_values
    
    def przelewy24_get_form_action_url(self, cr, uid, id, context=None):
        acquirer = self.browse(cr, uid, id, context=context)
        return self._get_przelewy24_urls(cr, uid, acquirer.environment, context=context)['przelewy24_form_url']
    