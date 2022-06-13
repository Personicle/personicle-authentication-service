import asyncio
import json
import requests
import jwt
import os
from okta_jwt_verifier import AccessTokenVerifier
from config import OKTA_TOKENS, OKTA_ENDPOINTS, OKTA_GROUPS
loop = asyncio.get_event_loop()

def get_token(request):
    return request.headers.get("Authorization").split("Bearer ")[1]

def get_audience(request):
    token = get_token(request)
    decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=["RS256"])
    return decoded_token['aud']

def get_scopes(request):
    token = get_token(request)
    decoded_token = jwt.decode(token, options={"verify_signature": False},algorithms=["RS256"])
    return decoded_token['scp']

def is_user_physician(request,user_id):
 
    token_valid = is_authorized(request)
    if token_valid:
        headers = {'Authorization': f"{OKTA_TOKENS['GET_USER_GROUP_TOKEN']}"}
        
        res = requests.get(f"{OKTA_ENDPOINTS['USER_ENDPOINT']}/{user_id}/groups", headers=headers)
        for g in res.json():
            if g['id'] == f"{OKTA_GROUPS['PHYSICIAN_GROUP']}":
                return True
        
    return False
def match_scopes(requested_scopes, valid_scopes):
    for scope in requested_scopes:
        if scope not in valid_scopes:
            return False
    return True

def get_user_info(request,audience):
    token = get_token(request)
    headers = {'Authorization': 'Bearer ' + token}
    if audience == "thirdparty":
        user_info = requests.get(os.environ['CLIENT_USERINFO_URI'], headers=headers)
    else:
        user_info = requests.get(os.environ['USER_INFO_URI'], headers=headers)
    real_user_id = user_info.json()['sub']
    
    return real_user_id

def is_authorized(request):
    try:    
        token = get_token(request)
        audience  = get_audience(request)
        
        if audience == 'thirdparty':
            return is_access_token_valid(token, os.environ['CLIENT_ISSUER'],audience)
        
        return is_access_token_valid(token, os.environ['ISSUER'],audience)
       

    except Exception:
        return False


def is_access_token_valid(token, issuer,audience):
    jwt_verifier = AccessTokenVerifier(issuer=issuer, audience=audience)
    try:
        loop.run_until_complete(jwt_verifier.verify(token))
        return True
    except Exception:
        return False


# def load_config(fname='client_secrets.json'):
#     config = None
#     with open(fname) as f:
#         config = json.load(f)
#     return config


# config = load_config()
