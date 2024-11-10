from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class mongoConnection():
    def create_connection (self):
        uri = "mongodb+srv://<username>:<db>@cluster0.wbcds.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        try: 
            client.admin.command('ping')
            return client
        except Exception as e:
            print(e)