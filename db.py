import os

from pymongo import MongoClient

class DbMongo:
    def save_oauth(self, id, token):
        client = MongoClient(os.environ.get('MONGOLAB_URI'))
        db = client.get_default_database()
        db.customers.save({'_id': id,
                           'token': token})

    def get_oauth_token(self, id):
        client = MongoClient(os.environ.get('MONGOLAB_URI'))
        db = client.get_default_database()
        customer = db.customers.find_one({'_id': id})
        return customer['token']
        
    
