import datetime
import uuid

class Folder:
    def __init__(self, folder_name, summary, user_id):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.folder_name = folder_name
        self.last_synced_at = datetime.datetime.now()
        self.summary = summary
        self.web_urls = []
        self.image_urls = []
        self.download_urls = []

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'folder_name': self.folder_name,
            'last_synced_at': str(self.last_synced_at),
            'summary': self.summary,
            'web_urls': self.web_urls,
            'image_urls': self.image_urls,
            'download_urls': self.download_urls
        }

    @classmethod
    def from_dict(cls, data):
        folder = cls(data['folder_name'], data['summary'], data['user_id'])
        if 'id' in data: folder.id = data['id']
        if 'created_at' in data: folder.created_at = data['created_at']
        if 'updated_at' in data: folder.updated_at = data['updated_at']
        if 'web_urls' in data: folder.web_urls = data['web_urls']
        if 'image_urls' in data: folder.image_urls = data['image_urls']
        if 'download_urls' in data: folder.download_urls = data['download_urls']

        return folder
