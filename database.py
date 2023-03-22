import pymongo
from config import Config

class BroadcastDB:
    
    def __init__(self, uri):
        self.dbclient = pymongo.MongoClient(uri)
        self.database = self.dbclient['PremiumBotz']
        self.user_data = self.database['users']
    
    
    
    async def present_user(self, user_id : int):
        found = self.user_data.find_one({'_id': user_id})
        return bool(found)
    
    async def add_user(self, user_id: int):
        self.user_data.insert_one({'_id': user_id})
        return
    
    async def del_user(self, user_id: int):
        self.user_data.delete_one({'_id': user_id})
        return

    async def full_userbase(self):
        user_docs = self.user_data.find()
        user_ids = []
        for doc in user_docs:
            user_ids.append(doc['_id'])
            
        return user_ids    

db = BroadcastDB(Config.DATABASE_URI)        
