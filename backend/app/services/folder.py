from models.folder import Folder
from app import db
from utils.utils import jsonify_document
from bson import ObjectId

class FolderService:
    def __init__(self):
        if 'folders' not in db.list_collection_names():
            db.create_collection('folders')
        self.collection = db.get_collection('folders')

    def create_folder(self, user_id, name, summary):
        folder = self.get_folder_by_name(name)
        if folder:
            return folder

        folder = Folder(user_id, name, summary)
        result = self.collection.insert_one(folder.to_dict())
        inserted_id = result.inserted_id
        folder = self.collection.find_one({'_id': ObjectId(inserted_id)})

        return jsonify_document(folder)

    def get_folders_by_user_id(self, user_id):
        folders = list(self.collection.find({'user_id': user_id}))
        return jsonify_document(folders)

    def get_folder_by_id(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        return jsonify_document(folder)

    def get_folder_by_name(self, folder_name):
        folder = self.collection.find_one({'name': folder_name})
        return jsonify_document(folder)

    def update_folder_by_id(self, folder_id, data):
        result = self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': data})
        if result.modified_count > 0:
            updated_folder = self.collection.find_one({'_id': ObjectId(folder_id)})
            return jsonify_document(updated_folder)
        else:
            return None

    def delete_folder_by_id(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        self.collection.delete_one({'_id': ObjectId(folder_id)})
        return jsonify_document(folder)

    def get_web_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        return folder['web_urls']

    def get_image_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        return folder['image_urls']

    def get_download_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        return folder['download_urls']

    def add_web_urls(self, folder_id, new_web_urls):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['web_urls'].extend(new_web_urls)
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)

    def add_image_urls(self, folder_id, new_image_urls):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['image_urls'].extend(new_image_urls)
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)

    def add_download_urls(self, folder_id, new_download_urls):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['download_urls'].extend(new_download_urls)
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)

    def delete_web_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['web_urls'] = []
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)

    def delete_image_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['image_urls'] = []
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)

    def delete_download_urls(self, folder_id):
        folder = self.collection.find_one({'_id': ObjectId(folder_id)})
        if not folder:
            return None
        folder['download_urls'] = []
        self.collection.update_one({'_id': ObjectId(folder_id)}, {'$set': folder})
        return jsonify_document(folder)
