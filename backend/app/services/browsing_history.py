from app import db
from utils.utils import jsonify_document
from bson import ObjectId

class BrowsingHistoryService:
    def __init__(self):
      if 'browsing_history' not in db.list_collection_names():
        db.create_collection('browsing_history')
      self.collection = db.get_collection('browsing_history')

    def get_browsing_history_by_ip(self, ip):
      browsing_history = list(self.collection.find({'ip': ip}))
      return jsonify_document(browsing_history)

    def add_browsing_history(self, browsing_history):
      result = self.collection.insert_many(browsing_history)
      inserted_ids = result.inserted_ids
      browsing_history = list(self.collection.find({'_id': {'$in': inserted_ids}}))
      return jsonify_document(browsing_history)

    def clean_browsing_history_by_ip(self, ip):
      result = self.collection.delete_many({'ip': ip})
      return result.deleted_count
