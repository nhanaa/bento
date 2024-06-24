from app import db
from utils.utils import jsonify_document
from bson import ObjectId

class DownloadsService:
  def __init__(self):
    if 'downloads' not in db.list_collection_names():
      db.create_collection('downloads')
    self.collection = db.get_collection('downloads')

  def get_downloads_by_ip(self, ip):
    downloads = list(self.collection.find({'ip': ip}))
    return jsonify_document(downloads)

  def add_downloads(self, downloads):
    result = self.collection.insert_many(downloads)
    inserted_id = result.inserted_ids
    downloads = list(self.collection.find({'_id': {'$in': inserted_id}}))
    return jsonify_document(downloads)

  def clean_downloads_by_ip(self, ip):
    result = self.collection.delete_many({'ip': ip})
    return result.deleted_count
