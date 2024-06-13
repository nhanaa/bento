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
            'folder_name': self.folder_name,
            'last_synced_at': self.last_synced_at,
            'summary': self.summary,
            'web_urls': self.web_urls,
            'image_urls': self.image_urls,
            'download_urls': self.download_urls
        }

    @classmethod
    def from_dict(cls, data):
        folder = cls(data['folder_name'], data['summary'])
        return folder
