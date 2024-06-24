from utils.search import SearchEngine

def getUserData(id):
    return [
        ['~/projects/bento/app.py', 'init python flask project'],
        ['~/documents/cv/resume.pdf', 'job application for fullstack AI and python'],
        ['~/documents/secrets/wallet.xls', 'money funding transaction money'],
    ]

class SearchService:
    def search(self, query):
        se = SearchEngine()
        se.seed('file', getUserData(1))

        return se.query('file', query)