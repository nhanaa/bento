from bson import ObjectId

def jsonify_document(document):
    if isinstance(document, list):
        for doc in document:
            doc['_id'] = str(doc['_id'])
    elif isinstance(document, dict):
        document['_id'] = str(document['_id'])
    return document
