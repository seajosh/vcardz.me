#!/usr/bin/env python
import os, sys, time

# Flask:
from flask import Flask, render_template, request, redirect, make_response, url_for, flash, session, g
# from flaskext.oauth import OAuth
from flask_oauth import OAuth
from flask_openid import OpenID

# import flaskext.openid
from openidmongodb import MongoDBStore

# Serialization
import json, base64

# MongoDB and BSON util
from pymongo import Connection

# UUID 
import uuid

# Simple configuration and helpers
import config
from helpers import *
# from kombu import BrokerConnection, Exchange, Queue

# Setup Flask web app
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) 
app = Flask(__name__, static_folder=os.path.join(PROJECT_ROOT, 'static'), static_url_path='/static')
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
oauth = OAuth()
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Setup Google OAuth Credentials
from urllib2 import Request, urlopen, URLError
import atom
import gdata.auth
import gdata.gauth
import gdata.contacts.data
import gdata.contacts.client
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.google.com/m8/feeds https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=config.GOOGLE_CLIENT_ID,
                          consumer_secret=config.GOOGLE_CLIENT_SECRET)

def oid_store_factory():
  return MongoDBStore(host = 'localhost',
                         port = 27017,
                         db = 'openid',
                         associations_collection = 'associations',
                         nonces_collection = 'nonces')

oid = OpenID(app, store_factory = oid_store_factory)


# Setup MongoDB
mongo = Connection(config.MONGO_URL)
db_name = 'reconcil' # os.environ['MONGODB']
db = getattr(mongo, db_name) # enables db_name to be configurable 
contacts_db = db.contacts

# Setup RabbitMQ
# rabbitmq = BrokerConnection(os.environ['RABBITMQ_URL'])
# reconcil_exchange = Exchange("reconcil", "direct", durable=True)
# contacts_queue = Queue("contacts", exchange=reconcil_exchange, routing_key="contacts")
# contacts_queue(rabbitmq.channel()).declare()


@app.before_request
def lookup_current_user():
  g.user = None
  if 'openid' in session:
    pass

# / Route displays upload form and oauth button
@app.route('/')
def index():
  log("AT INDEX")
  access_token = session.get('access_token')
  if access_token is None:
    log("NO ACCESS TOKEN")
    return render_template('partials/index.html', access_token=access_token)
  log("HAS ACCESS TOKEN")
  access_token = access_token[0]
  headers = {'Authorization': 'OAuth '+access_token}
  
  email_req = Request('https://www.googleapis.com/userinfo/email?alt=json', None, headers)
  email_res = urlopen(email_req)
  email_struct = json.loads(email_res.read())
  email_address = email_struct['data']['email']
  log("EMAIL ADDRESS: " + email_address)
  return render_template('partials/index.html', access_token=access_token, email_address=email_address)

@app.route('/login', methods=['GET','POST'])
def login():
  callback=url_for('authorized', _external=True)
  return google.authorize(callback=callback)


@app.route('/test/')
def test():
  log("AT TEST/INDEX")
  return render_template('partials/test/index.html')

@app.route('/test/site_login', methods=['GET','POST'])
@oid.loginhandler
def site_login():
  if g.user is not None:
    return redirect(oid.get_next_url())
  if request.method == 'POST':
    openid = request.form.get('openid')
    if openid:
      return oid.try_login(openid, ask_for = ['email', 'fullname', 'nickname'])
  return render_template('partials/test/login.html', 
                         oid_url = flaskext.openid.COMMON_PROVIDERS['google'],
                         next=oid.get_next_url(), 
                         error=oid.fetch_error())  


@app.route('/test/app')
def site_app():
  # if g.user is not None:
  #   return render_template('partials/test/app.html')
  # return redirect(url_for('test'))
  # if g.user is None:
  #   return redirect(url_for('site_login'))
  # log(g.user)
  
  return render_template('partials/test/app.html',
                         isuser=(g.user is None))
  

@oid.after_login
def after_login(resp):
  session['openid'] = resp.identity_url
  log("new openid => %s" % session['openid'])
  customers = db.customers
  user = customers.find_one({'openid': session['openid']})
  if not user:
    customers.insert({'email': resp.email,
                      'name': resp.fullname or resp.nickname,
                      'openid': session['openid']})
  return redirect(url_for('site_app'))

@app.route('/logout')
def logout():
  session.pop('access_token', None)
  return redirect(url_for('index'))

@app.route(config.REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
  access_token = resp['access_token']
  session['access_token'] = access_token, ''
  print str(session)
  return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
  return session.get('access_token')

# Export the processed contacts as vcards
@app.route("/vcards/export/<unique_id>", methods=['GET', 'POST'])
def vcards(unique_id):
  log("querying contacts for <" + unique_id + "> to see if they're processed...")
  contacts = contacts_db.find_one({'uuid': unique_id, 'status': 'done'})
  log("retrieved contacts, evaluating result...")
  if contacts:
    log("processed contacts found, parsing vcards")
    log("make_response")
    response = make_response(contacts['scrub'])
    response.headers['Content-Disposition'] = 'attachment; filename=contacts.vcf'
    response.headers['Content-Type'] = 'text/vcard'
    log("returning vcards")
    return response
  else:
    log("index.py: vcards are not yet ready...")
    return render_template('partials/waiting.html')

# Export the processed contacts as vcards
@app.route("/vcards/mobile/<unique_id>", methods=['GET', 'POST'])
def vcards_mobile(unique_id):
  log("querying contacts for <" + unique_id + "> to see if they're processed...")
  contacts = contacts_db.find_one({'uuid': unique_id, 'status': 'done'})
  log("retrieved contacts, evaluating result...")
  if contacts:
    log("processed contacts found, returning vcards")
    return contacts['scrub']
  else:
    return 'wait'

# Stub for uploading from Titanium App
@app.route("/mobile", methods=['GET', 'POST'])
def mobile():
  log("mobile upload")
  log("request.form: " + str(request.form))
  log(str(request))
  log("checking form for email address")
  if(request.form['email_address']):
    log("got email address %s" % (request.form['email_address']))
    email_address = request.form['email_address']
    if(request.form['vcards']):
      log("got vcards from form")
      vcards = request.form['vcards']
    else:
      log("ERROR no vcards")
      return 'ERROR'
  else:
    log("ERROR no email address")
    return 'ERROR'
  # Only accept POSTs
  log("Evaluating POST")
  if request.method == 'POST':
    # Make a unique UUID for this request and create a record
    log("creating a UUID.")
    unique_id = uuid.uuid4().urn
    log("inserting address book to mongo: %s" % (unique_id))
    contacts_db.insert({'email': email_address, 'vcards': vcards, 'status': 'raw', 'uuid': unique_id})
    
    # Produce MQ event for workers to process.
    log("event producer setup")
    producer = rabbitmq.Producer(exchange=reconcil_exchange, serializer="json", routing_key="contacts")
    log("creating download_url")
    with app.test_request_context():
      download_url = url_for('vcards', unique_id=unique_id, _external=True)
    
    log("publishing event")
    producer.publish({'email': email_address, 'uuid': unique_id, 'download_url': download_url})
    log("published event")
    return unique_id
  # Not an allowed filetype
  else:
    log("Error! GET not allowed.")
    return 'ERROR'

# Upload form processor - importing vcards for processing, storing to Mongo, throwing a RabbitMQ event for processing.
@app.route("/upload", methods=['GET', 'POST'])
def upload():
  log("upload")
  # access_token = session.get('access_token')
  # if access_token is None:
  #   return 'error'
  if request.form['email_address']:
    log("got email address %s" % (request.form['email_address']))
    email_address = request.form['email_address']
  else:
    log("ERROR no email address")
    # return 'ERROR'
    email_address = 'jwatts@cowboy'
  # Only accept POSTs
  if request.method == 'POST':
    log("got post")
    file = request.files['file']
    log("file = request.files")
    if file and allowed_file(file.filename):
      log("file and allowed_file")
      content = file.read()
      
      # Make a unique UUID for this request and create a record 
      log("creating a UUID.")
      unique_id = uuid.uuid4().urn
      log("inserting address book to mongo: %s" % (unique_id))
      contacts_db.insert({'email': email_address, 'vcards': content.decode('utf-8'), 'status': 'raw', 'uuid': unique_id, 'access_token': access_token})
      
      # # Produce MQ event for workers to process.
      # log("event producer setup")
      # producer = rabbitmq.Producer(exchange=reconcil_exchange, serializer="json", routing_key="contacts")
      # log("creating download_url")
      # with app.test_request_context():
      #   download_url = url_for('vcards', unique_id=unique_id, _external=True)
      
      # log("publishing event")
      # producer.publish({'email': email_address, 'uuid': unique_id, 'download_url': download_url})
      # log("published event")
      # return redirect('/vcards/export/' + unique_id)

    # Not an allowed filetype
    else:
      #flash('Please select a file for upload.') 
      return redirect('/')
  # GET not allowed
  else:
    log("Error! GET not allowed.")
    return 'ERROR'

def GetContactsFeed(feed):
  if not feed.entry:
    print '\nNo contacts in feed.\n'
    return 0
  for i, entry in enumerate(feed.entry):
    if not entry.name is None:
      family_name = entry.name.family_name is None and " " or entry.name.family_name.text
      print '\n%s %s: %s - %s' % (i+1, entry.name.full_name.text, entry.name.given_name.text, family_name)
    else:
      print '\n%s %s (title)' % (i+1, entry.title.text)
    if entry.content:
      print '    %s' % (entry.content.text)
    for p in entry.structured_postal_address:
      print '    %s' % (p.formatted_address.text)
    # Display the group id which can be used to query the contacts feed.
    print '    Group ID: %s' % entry.id.text
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlob()
      print '    Extended Property %s: %s' % (extended_property.name, value)
    for user_defined_field in entry.user_defined_field:
      print '    User Defined Field %s: %s' % (user_defined_field.key, user_defined_field.value)
  return len(feed.entry)

# Bind to ENV['PORT'] and run.
if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  # port = int(os.environ.get('PORT', 5000))
  port = 5000
  app.debug = True
  use_debugger = True
  app.run(host='0.0.0.0', port=port)
