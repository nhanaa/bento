from flask import jsonify
from models.folder import Folder
from utils.db import CosmosDB
import uuid

class FolderService:
    def __init__(self):
        self.container = CosmosDB.get_container('Folders')

    def create_folder(self, name, summary):
        folder = Folder(name, summary)
        folder.id = str(uuid.uuid4())
        self.container.create_item(body=folder.to_dict())
        return folder

    def get_folders(self):
        query = "SELECT * FROM c"
        items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        return [Folder.from_dict(item).to_dict() for item in items]
    
    def get_folder(self, query):
        items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        if not items:
            return None
        folder = Folder.from_dict(items[0])
        return folder.to_dict()

    def get_folder_by_id(self, folder_id):
        query = f"SELECT * FROM Folders u WHERE u.id = '{folder_id}'"
        return self.get_folder(query)
    
    def get_folder_by_name(self, folder_name):
        query = f"SELECT * FROM Folders u WHERE u.name = '{folder_name}'"
        return self.get_folder(query)
    
    def get_web_urls(self, folder_name):
        folder = self.get_folder_by_name(folder_name)
        return folder.web_urls
    
    def get_image_urls(self, folder_name):
        folder = self.get_folder_by_name(folder_name)
        return folder.image_urls
    
    def get_download_urls(self, folder_name):
        folder = self.get_folder_by_name(folder_name)
        return folder.download_urls
    
    def add_web_urls(self, folder_name, new_web_urls):
        folder = self.get_folder_by_name(folder_name)
        folder.web_urls.extend(new_web_urls)
        return folder
    
    def add_image_urls(self, folder_name, new_image_urls):
        folder = self.get_folder_by_name(folder_name)
        folder.image_urls.extend(new_image_urls)
        return folder

    def add_download_urls(self, folder_name, new_download_urls):
        folder = self.get_folder_by_name(folder_name)
        folder.download_urls.extend(new_download_urls)
        return folder

    def delete_web_urls(self, folder_name, web_url):
        folder = self.get_folder_by_name(folder_name)
        folder.web_urls.remove(web_url)
        return folder
    
    def delete_image_urls(self, folder_name, image_url):
        folder = self.get_folder_by_name(folder_name)
        folder.image_urls.remove(image_url)
        return folder
    
    def delete_download_urls(self, folder_name, download_url):
        folder = self.get_folder_by_name(folder_name)
        folder.download_urls.remove(download_url)
        return folder
    
    
        
