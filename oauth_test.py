import sys, os
print os.getcwd() + '/src/lib/flask-oauth'
sys.path.append(os.getcwd() + '/src/lib/flask-oauth')
from flask import Flask, redirect, url_for, flash, session
from flaskext.oauth import OAuth
import atom
import gdata.auth
import gdata.gauth
import gdata.contacts.data
import gdata.contacts.client


# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '771722919601.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'cDTT13VO98029ag6lgxR_h9a'
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console

SECRET_KEY = 'AIzaSyDirMR-4NtUE-10nNsTqcKrRFhfUw5W8Ck'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.google.com/m8/feeds https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    
    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
    
    headers = {'Authorization': 'OAuth '+access_token}
    
    req = Request('https://www.google.com/m8/feeds/contacts/default/full',
                  None, headers)
    print "Auth token class: " + str(access_token.__class__)
    auth_token = gdata.gauth.AuthSubToken(access_token)
    contacts_client = gdata.contacts.client.ContactsClient(auth_token=auth_token)
    feed = contacts_client.GetContacts()
    GetContactsFeed(feed)
    print feed
    try:
        res = urlopen(req)
    except URLError:
        return res.read()
    
    return res.read()

@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    print str(session)
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')

def main():
    app.run()

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

if __name__ == '__main__':
    main()