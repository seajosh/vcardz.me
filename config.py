# config.py - a configuration file for index.py
ALLOWED_EXTENSIONS=set(['vcf', 'VCF', 'Vcf', 'csv', 'CSV', 'Csv', 'pst', 'PST', 'Pst'])
MAX_CONTENT_LENGTH=16 * 1024 * 1024
MAX_INSTANT_SIZE=150000
GOOGLE_CLIENT_ID='771722919601.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'cDTT13VO98029ag6lgxR_h9a'
REDIRECT_URI = '/authorized'  # one of the Redirect URIs from Google APIs console
SECRET_KEY = 'AIzaSyDirMR-4NtUE-10nNsTqcKrRFhfUw5W8Ck'
DEBUG = True

MONGO_URL = 'mongodb://localhost'
