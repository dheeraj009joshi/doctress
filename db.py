from pymongo import MongoClient


uri = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['doctress']
collection = db['users']
service_provider_collection = db['service_provider']
# a=collection.update_many({}, {"$unset": {"verified": ""}})
# print(a)
# query = {"$or": [{"account_status": {"$exists": False}}, {"membership": {"$exists": False}}]}
# update_data = {'$set': {"account_status": "pending", "membership": 0}}
# # Update documents
# update_result = collection.update_many(query, update_data)

# # Print update result
# print("Matched", update_result.matched_count, "documents")
# print("Modified", update_result.modified_count, "documents")