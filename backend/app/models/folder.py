import datetime

class Folder:
    def __init__(self, user_id, name, summary):
        self.user_id = user_id
        self.name = name
        self.last_synced_at = datetime.datetime.now()
        self.summary = summary
        self.web_urls = []
        self.image_urls = []
        self.download_urls = []

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'last_synced_at': self.last_synced_at,
            'summary': self.summary,
            'web_urls': self.web_urls,
            'image_urls': self.image_urls,
            'download_urls': self.download_urls
        }

    @classmethod
    def from_dict(cls, data):
        folder = cls(data['name'], data['summary'])
        return folder
