import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import flask
import db_adapter, json

from collections import namedtuple

TestRequest = namedtuple('TestRequest', ['remote_addr', 'args'])

def get_response_content(request, action_function):
    if request.args and 'id' in request.args and 'ip' in request.args:
        return json.dumps(action_function(request.args.get('id'), request.args.get('ip')))
    else:
        return json.dumps({'status': db_adapter.STATUS_FAILURE, 'message': 'Not found arg `id` or `ip` in request'})

def act(request, action_function):
    resp = flask.Response(get_response_content(request, action_function))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,OPTIONS,POST,PUT'
    resp.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'
    return resp
