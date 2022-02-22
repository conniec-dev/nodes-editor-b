import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "nodes-editor",
})

db = firestore.client()

doc_ref = db.collection(u'drawflowdiagrams').document(u'drawflowdiagram')
doc_ref.set({
    u'name': u'sum_program',
    u'drawflow_output': 'content',
    u'date': firestore.SERVER_TIMESTAMP
})

