import config
import sys, os
# from kombu import BrokerConnection, Consumer, Producer

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in config.ALLOWED_EXTENSIONS

def log(message):
  sys.stderr.write(__file__ + ": " + message + "\n")
