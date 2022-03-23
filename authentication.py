from flask import Flask, jsonify, request
from okta_authenticate.helpers import is_authorized , is_user_valid

app = Flask(__name__)

@app.route('/authenticate',methods=["GET", "POST"])
def authenticate():
    
    if not is_user_valid(request) or not is_authorized(request):
        return "Unauthorized", 401
   
    return jsonify({"message": True})

@app.route('/', methods=['GET','POST'])
def index():
    
    return jsonify({"message": "Personicle authentication server"})

if __name__ == '__main__':
    app.run()