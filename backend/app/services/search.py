from utils.search import SearchEngine
from services.folder import FolderService

folder_service = FolderService()

def getUserData(user_id):
    def mapField(folder):
        return [folder['folder_name'], folder['folder_name'] + ' ' + folder['summary']]
    return map(mapField, folder_service.get_folders_by_user_id(user_id))

class SearchService:
    def search(self, user_id, query):
        se = SearchEngine()
        se.seed('file', getUserData(user_id))

        return se.query('file', query)