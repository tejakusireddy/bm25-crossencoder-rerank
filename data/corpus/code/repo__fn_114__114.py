def create_permission_request(self, customer, pos_id, pos_tid, scope,
                                  ledger=None, text=None, callback_uri=None,
                                  expires_in=None):
        
        arguments = {'customer': customer,
                     'pos_id': pos_id,
                     'pos_tid': pos_tid,
                     'scope': scope,
                     'ledger': ledger,
                     'text': text,
                     'callback_uri': callback_uri,
                     'expires_in': expires_in}
        return self.do_req('POST',
                           self.merchant_api_base_url + '/permission_request/',
                           arguments).json()