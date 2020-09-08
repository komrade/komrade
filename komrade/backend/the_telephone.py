# internal imports
import os,sys; sys.path.append(os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')),'..')))
from komrade import *
from komrade.backend import *

### ACTUAL PHONE CONNECTIONS
class TheTelephone(Operator):
    """
    API client class for Caller to interact with The Operator.
    """
    def __init__(self, caller=None):
        global OPERATOR_KEYCHAIN,TELEPHONE_KEYCHAIN
        print('OP???',OPERATOR_KEYCHAIN)
        print('PH???',TELEPHONE_KEYCHAIN)
        
        super().__init__(
            name=TELEPHONE_NAME,
            path_crypt_keys=PATH_CRYPT_CA_KEYS,
            path_crypt_data=PATH_CRYPT_CA_KEYS
        )
        
        if not TELEPHONE_KEYCHAIN or not OPERATOR_KEYCHAIN:
            OPERATOR_KEYCHAIN,TELEPHONE_KEYCHAIN = connect_phonelines()
        
        print('OP2???',OPERATOR_KEYCHAIN)
        print('PH2???',TELEPHONE_KEYCHAIN)
        # stop
        
        self.caller=caller
        self._keychain = TELEPHONE_KEYCHAIN
        print(type(self._keychain), self._keychain)
        

    def send_and_receive(self,msg_b64_str_esc):
        URL = OPERATOR_API_URL + msg_b64_str_esc + '/'
        self.log("DIALING THE OPERATOR:",URL)
        ringring=komrade_request(URL)
        if ringring.status_code==200:

            # response back from Operator!
            encr_str_response_from_op = ringring.text
            self.log('encr_str_response_from_op',encr_str_response_from_op)

            return encr_str_response_from_op.encode()
        else:
            self.log('!! error in request',ringring.status_code,ringring.text)
            return None

    def ring_ring(self,msg_encr_caller2caller_caller2phone):

        # ring 1: encrypt
        msg_encr_caller2caller_caller2phone_phone2phone = self.package_msg_to(
            msg_encr_caller2caller,
            self.op
        )
        self.log('final form of encr msg!',msg_encr_caller2caller_caller2phone_phone2phone)

        # ring 2: dial and get response
        msg_encr_caller2caller_caller2phone_phone2phone = self.send_and_receive(msg_encr_caller2caller_phone2phone)
        msg_encr_caller2caller_caller2phone_phone2phone: return

        # ring 3: decrypt
        msg_encr_caller2caller_caller2phone = self.unpackage_msg_from(
            msg_encr_caller2caller_caller2phone_phone2phone,
            self.op
        )

        return msg_encr_caller2caller_caller2phone

    
def test_call():
    caller = Caller('marx33') #Caller('marx')
    # caller.boot(create=True)
    # print(caller.keychain())
    # phone = TheTelephone()
    # req_json = {'_please':'forge_new_keys','name':name, 'pubkey_is_public':pubkey_is_public}}
    # req_json_s = jsonify(req_json)
    # res = phone.req({'forge_new_keys':{'name':'marx', 'pubkey_is_public':True}})
    # print(res)
    # asyncio.run(caller.get_new_keys())
    x=caller.get_new_keys(passphrase='1869')

    print('YEAH COOL',x)

## main
if __name__=='__main__': test_call()