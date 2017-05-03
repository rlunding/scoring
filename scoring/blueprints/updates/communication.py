import hmac
import hashlib
import json
import base64

SHARED_SECRET = b'sup3rs3cr3t!!'

def sign_json(json_to_sign):
    """
    Create a hmac for the json data and secret key

    :return:
    """
    signature = hmac.new(SHARED_SECRET, msg=json_to_sign.encode("utf-8"), digestmod=hashlib.sha512).hexdigest()
    #encoded_signature = base64.urlsafe_b64encode(signature)
    return signature

def verify_json(json_to_verify, signature):
    return hmac.compare_digest(signature, sign_json(json_to_verify))
