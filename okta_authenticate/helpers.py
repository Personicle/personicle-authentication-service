import asyncio
import json

from okta_jwt_verifier import AccessTokenVerifier, IDTokenVerifier
loop = asyncio.get_event_loop()

def is_authorized(request):
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        return is_access_token_valid(token, config["issuer"])
    except Exception:
        return False


def is_access_token_valid(token, issuer):
    jwt_verifier = AccessTokenVerifier(issuer=issuer, audience='api://default')
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