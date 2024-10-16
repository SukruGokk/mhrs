import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# database connection
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mhrs-randevu.firebaseio.com'
})

firestoreDb = firestore.client()

class patients():
    def __init__(self):
        self.patients = list(firestoreDb.collection(u'patients').stream())

var = patients()

# read collection
def read_collection(collection):
    try:
        if collection == 'patients':
            return var.patients
        else:
            patients = list(collection_ref.where(filter = FieldFilter(key, u'==', value)).stream())
            return patients

    except Exception as e:
        print(e)

# get specific document
def document_query(collection, key, value):
    try:
        collection_ref = firestoreDb.collection(u'{}'.format(collection))
        documents = list(collection_ref.where(filter = FieldFilter(key, u'==', value)).stream())
        return documents
    except Exception as e:
        print(e)

# update a field
def update_document(collection, id, data):
    try:
        collection = firestoreDb.collection(u'{}'.format(collection))
        document = collection.document(id)
        document.update(data)
        if collection == 'patients':
            var.patients = list(firestoreDb.collection(u'patients').stream())

    except Exception as e:
        print(e)

# create new document
def add_document(collection, data):
    try:
        collection = firestoreDb.collection(u'{}'.format(collection))
        collection.add(data)
        if collection == 'patients':
            var.patients = list(firestoreDb.collection(u'patients').stream()) 

    except Exception as e:
         print(e)

# delete document
def delete_document(collection, id):
    try:
        collection = firestoreDb.collection(u'{}'.format(collection))
        document = collection.document(id)
        document.delete()
        if collection == 'patients':
            var.patients = list(firestoreDb.collection(u'patients').stream())

    except Exception as e:
        print(e)

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        print(change.type.name)
