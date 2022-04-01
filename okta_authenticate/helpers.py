import asyncio
import json
import requests
import jwt
from okta_jwt_verifier import AccessTokenVerifier
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

def match_scopes(requested_scopes, valid_scopes):
    for scope in requested_scopes:
        if scope not in valid_scopes:
            return False
    return True

def get_user_info(request,audience):
    token = get_token(request)
    headers = {'Authorization': 'Bearer ' + token}
    if audience == "thirdparty":
        user_info = requests.get(config["client_userinfo_uri"], headers=headers)
    else:
        user_info = requests.get(config["userinfo_uri"], headers=headers)
    real_user_id = user_info.json()['sub']
    
    return real_user_id

def is_authorized(request):
    try:    
        token = get_token(request)
        audience  = get_audience(request)

        if audience == 'thirdparty':
            return is_access_token_valid(token, config["client_issuer"],audience)

        return is_access_token_valid(token, config["issuer"],audience)
    except Exception:
        return False


def is_access_token_valid(token, issuer,audience):
    jwt_verifier = AccessTokenVerifier(issuer=issuer, audience=audience)
    try:
        loop.run_until_complete(jwt_verifier.verify(token))
        return True
    except Exception:
        return False


def load_config(fname='client_secrets.json'):
    config = None
    with open(fname) as f:
        config = json.load(f)
    return config


config = load_config()