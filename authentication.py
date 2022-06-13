from distutils.log import debug
from flask import Flask, jsonify, request
from okta_authenticate.helpers import is_authorized, get_user_info, get_scopes, match_scopes, get_audience, is_user_physician
import os
import collections
import requests
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists 
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from config import DB_CONFIG
app = Flask(__name__)
engine = create_engine("postgresql://{username}:{password}@{dbhost}/{dbname}".format(username=DB_CONFIG['USERNAME'], password=DB_CONFIG['PASSWORD'],
                                                                                                         dbhost=DB_CONFIG['HOST'], dbname=DB_CONFIG['NAME']))
Base = declarative_base(engine)

def loadSession():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = loadSession()

meta_data = db.MetaData(bind=engine)
db.MetaData.reflect(meta_data)
physician_users = meta_data.tables['physician_users']

@app.route('/authenticate',methods=["GET", "POST"])
def authenticate():
    requested_scopes = request.args.get('scopes')
    default_scopes = ['openid','email','profile']
    requested_scopes_list = requested_scopes.split(",") if requested_scopes is not None else default_scopes
    requested_scopes_list += default_scopes
    # print(requested_scopes_list)
    uid = request.args.get('user_id')
    if uid == "":
     uid = None
    
    if not is_authorized(request):
        return "Unauthorized", 401
    # check if access token belongs to physician
    audience = get_audience(request)
    user_id = get_user_info(request,audience)
    is_physician = is_user_physician(request,user_id)
    
    if is_physician and uid != None and uid!=user_id:
        #check if user_id(physician) has access to uid(patient) data
        mapping_exists = session.query(exists().where((physician_users.c.user_user_id == uid) & (physician_users.c.physician_user_id == user_id))).scalar()
        if mapping_exists:
            print(f"physician authorized to access data for user {uid}")
            return jsonify({"message": True, "user_id": uid}) ,200  # return user id for specifed patient
        else:
            print(f"physician NOT authorized to access data for user {uid}")
            return jsonify({"error": "Not authorized to view patient data"}) ,401
           
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
    app.run()
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(IDENTITY_SERVER_SETTINGS['HOST_URL'], port=IDENTITY_SERVER_SETTINGS['HOST_PORT'], debug=True)#, ssl_context='adhoc')
