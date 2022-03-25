from distutils.log import debug
from flask import Flask, jsonify, request
from okta_authenticate.helpers import is_authorized, get_user_info
from config import IDENTITY_SERVER_SETTINGS
import os

app = Flask(__name__)

@app.route('/authenticate',methods=["GET", "POST"])
def authenticate():
    
    if not is_authorized(request):
        return "Unauthorized", 401
    user_id = get_user_info(request)
    return jsonify({"message": True, "user_id": user_id})

@app.route('/', methods=['GET','POST'])
def index():
    
    return jsonify({"message": "Personicle authentication server"})

if __name__ == '__main__':
    app.run()
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(IDENTITY_SERVER_SETTINGS['HOST_URL'], port=IDENTITY_SERVER_SETTINGS['HOST_PORT'], debug=True)#, ssl_context='adhoc')
