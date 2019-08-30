import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random, os

PROJECT_ID = 'zyra-1537465980753'

COLLECTION_NAME = u'baneks'
ID_FIELD_NAME = u'id'
LIKES_FIELD_NAME = u'liked'
DISLIKES_FIELD_NAME = u'disliked'
TEXT_FIELD_NAME = u'text'

STATUS_SUCCESS = 'success'
STATUS_FAILURE = 'failure'
MAX_WRITES_PER_BATCH = 400

def select_random_anek_id():
    users_ref = db.collection(COLLECTION_NAME)
    docs = list(users_ref.stream())
    return random.choice(docs).id

def select_random_anek():
    id = select_random_anek_id()
    return db.collection(COLLECTION_NAME).document(id).get().to_dict(), id

def get_anti_field(field):
    if field == LIKES_FIELD_NAME:
        return DISLIKES_FIELD_NAME
    else:
        return LIKES_FIELD_NAME

def get_anti_field(field):
    if field == LIKES_FIELD_NAME:
        return DISLIKES_FIELD_NAME
    else:
        return LIKES_FIELD_NAME

def populate(id, ip, field):
    antifield = get_anti_field(field)
    ref = db.collection(COLLECTION_NAME).document(id)
    if ref.get().to_dict() is None:
        return {'status': STATUS_FAILURE, 'message': 'No such document'}
    populated = ref.get().to_dict()[field]
    antipopulated = ref.get().to_dict()[antifield]
    if not ip in populated:
        ref.update({
                field: populated + [ip],
                antifield: [i for i in antipopulated if i != ip]
            })
        return {'status': STATUS_SUCCESS, 'message': 'Updated'}
    else:
        return {'status': STATUS_FAILURE, 'message': 'Already done'}

def like(id, ip):
    return populate(id, ip, LIKES_FIELD_NAME)

def dislike(id, ip):
    return populate(id, ip, DISLIKES_FIELD_NAME)

def add_aneks(texts):
    collection = db.collection(COLLECTION_NAME)
    print(dir(collection))
    batch = db.batch()
    counter = 0
    for text in texts:
        batch.set(collection.document(), {
            TEXT_FIELD_NAME: text,
            LIKES_FIELD_NAME: [],
            DISLIKES_FIELD_NAME: []
        })
        if (counter % MAX_WRITES_PER_BATCH == 0):
            batch.commit()
            batch = db.batch()
        counter += 1


if os.environ['IN_CLOUD'] == 'true':
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
      'projectId': PROJECT_ID,
    })
else:
    cred = credentials.Certificate(os.environ['FIRESTORE_SERVICE_ACCOUNT_PATH'])
    firebase_admin.initialize_app(cred)

db = firestore.client()