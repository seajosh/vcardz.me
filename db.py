from pymongo import MongoClient

class DbMongo:
    def save_oauth(self, id, token):
        client = MongoClient('localhost', 27017)
        client.vcardz.customers.save({'_id': id,
                                      'token': token})

    def get_oauth_token(self, id):
        client = MongoClient('localhost', 27017)
        customer = client.vcardz.customers.find_one({'_id': id})
        return customer['token']
        
    
