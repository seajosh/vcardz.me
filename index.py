#!/usr/bin/env python

import json
import random
import os
import pickle
import string
from six import StringIO
import sys
import time

# Flask
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import session

# OAuth2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials

# requests / OAuth2
import requests
import requests_oauthlib
from requests_oauthlib import OAuth2
from requests_oauthlib import OAuth2Session

#
from db import DbMongo
from vcardz_data import builder
from vcardz_data.google import GoogleFeed

# Flask setup
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,
            static_folder=os.path.join(PROJECT_ROOT,
                                       'static'),
            static_url_path='/static')
app.secret_key = '\x84\xb2r\xd72\x0bX\xae\xcc\x80\xab\xe7w\x8e\xf5\xe5\xecP\xf0\xc3\x9c\x18\x1c\xfd'
app.debug = True

#
# utility routes
#
@app.route('/lib/<path:path>')
def route_static(path):
    temp = os.path.join('./static/lib/',
                        path)
    (head, tail) = os.path.split(temp)
    app.logger.debug('head => ' + head)
    app.logger.debug('tail => ' + tail)
    return send_from_directory(head + '/', tail)


#
# pages
# 
@app.route('/')
def index():
    # Create a state token to prevent request forgery.
    # Store it in the session for later validation.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    response = make_response(render_template('partials/index.html'))
    response.set_cookie('state', state)
    session['state'] = state
    return response

#
# REST endpoints
#
@app.route('/rest/v1/google/signin', methods=['POST'])
def google_signin():
    if request.cookies.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.get_json()
    app.logger.debug('code => ' + code)
    try:
        oauth_flow = flow_from_clientsecrets('config/google.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    app.logger.debug('upgraded authorization code')
    gplus_id = credentials.id_token['sub']
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    db = DbMongo()
    if stored_credentials is not None \
       and gplus_id == stored_gplus_id:
        db.save_oauth(gplus_id, pickle.dumps(credentials))
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # http://stackoverflow.com/questions/22915461/google-login-server-side-flow-storing-credentials-python-examples
    session['credentials'] = pickle.dumps(credentials)
    session['gplus_id'] = gplus_id
    app.logger.debug('gplus_id => ' + gplus_id)
    # db.save_oauth(gplus_id, credentials.access_token)
    db.save_oauth(gplus_id, pickle.dumps(credentials))
    session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Success connected user.',
                                        200))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/rest/v1/google/contacts')
def google_contacts():
    credentials = Credentials.from_json(session.get('credentials'))
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    db = DbMongo()
    credentials = pickle.loads(db.get_oauth_token(session['gplus_id']))
    client = requests.Session()
    client.headers.update({'Authorization': 'Bearer ' + credentials.access_token,
                           'GData-Version': '3.0'})
    client_response = client.get('https://www.google.com/m8/feeds/contacts/default/full')
    google = GoogleFeed(client_response.text)
    cards = [x.compact() for x in google]
    response = make_response(json.dumps(cards), 200)
    response.headers['Content-Type'] = 'application/json'
    return response



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0',
            port=port,
            ssl_context=('config/dev-vcardz.crt', 
                         'config/dev-vcardz.key'))

