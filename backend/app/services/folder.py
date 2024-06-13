from bson.objectid import ObjectId
from pymongo import MongoClient
from utils.db import MongoDB
from models.folder import Folder
import uuid

class FolderService:
    def __init__(self):
        self.collection = MongoDB.get_collection('Users')

    def create_folder(self, name, summary, user_id):
        folder = Folder(name, summary, user_id)
        folder.id = str(uuid.uuid4())
        self.collection.insert_one(folder.to_dict())
        return folder

    def get_folders_by_user_id(self, user_id):
        query = {"user_id": user_id}
        items = list(self.collection.find(query))
        return [Folder.from_dict(item).to_dict() for item in items]

    def get_folder_by_id(self, folder_id):
        query = {"_id": ObjectId(folder_id)}
        return self.get_folder(query)

    def get_folder_by_name(self, folder_name, user_id):
        query = {"name": folder_name, "user_id": user_id}
        return self.get_folder(query)

    def get_folder(self, query):
        item = self.collection.find_one(query)
        return Folder.from_dict(item) if item else None

    def get_web_urls(self, folder_name, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        return folder.web_urls if folder else []

    def get_image_urls(self, folder_name, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        return folder.image_urls if folder else []

    def get_download_urls(self, folder_name, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        return folder.download_urls if folder else []

    def add_web_urls(self, folder_name, new_web_urls, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.web_urls.extend(new_web_urls)
            self.update_folder(folder)
        return folder

    def add_image_urls(self, folder_name, new_image_urls, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.image_urls.extend(new_image_urls)
            self.update_folder(folder)
        return folder

    def add_download_urls(self, folder_name, new_download_urls, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.download_urls.extend(new_download_urls)
            self.update_folder(folder)
        return folder

    def delete_web_urls(self, folder_name, web_url, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.web_urls.remove(web_url)
            self.update_folder(folder)
        return folder

    def delete_image_urls(self, folder_name, image_url, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.image_urls.remove(image_url)
            self.update_folder(folder)
        return folder

    def delete_download_urls(self, folder_name, download_url, user_id):
        folder = self.get_folder_by_name(folder_name, user_id)
        if folder:
            folder.download_urls.remove(download_url)
            self.update_folder(folder)
        return folder

    def update_folder(self, folder):
        self.collection.update_one({"_id": ObjectId(folder.id)}, {"$set": folder.to_dict()})
