from utils.search import SearchEngine
from services.folder import FolderService

def getUserData(user_id):
    return FolderService.get_folders_by_user_id(user_id)

class SearchService:
    def search(self, user_id, query):
        se = SearchEngine()
        se.seed('file', getUserData(user_id))

        return se.query('file', query)