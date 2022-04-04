from distutils.log import debug
from flask import Flask, jsonify, request
from okta_authenticate.helpers import is_authorized, get_user_info, get_scopes, match_scopes, get_audience
import os
import collections

app = Flask(__name__)


@app.route('/authenticate',methods=["GET", "POST"])
def authenticate():
    requested_scopes = request.args.get('scopes')
    default_scopes = ['openid','email','profile']
    requested_scopes_list = requested_scopes.split(",") if requested_scopes is not None else default_scopes
    requested_scopes_list += default_scopes
    print(requested_scopes_list)
    if not is_authorized(request):
        return "Unauthorized", 401

    audience = get_audience(request)
    user_id = get_user_info(request,audience)
    valid_scopes = get_scopes(request)
    valid_scopes_set = set(valid_scopes)

    requested_scopes_set = set(requested_scopes_list)
    scopes_matched = match_scopes(requested_scopes_set,valid_scopes_set)
    if not scopes_matched and audience!='api://default':
        return jsonify({"message": "INVALID_SCOPES"}),403

    return jsonify({"message": True, "user_id": user_id})

@app.route('/', methods=['GET','POST'])
def index():
    
    return jsonify({"message": "Personicle authentication server"})

if __name__ == '__main__':
    app.run(debug=True)
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(IDENTITY_SERVER_SETTINGS['HOST_URL'], port=IDENTITY_SERVER_SETTINGS['HOST_PORT'], debug=True)#, ssl_context='adhoc')
