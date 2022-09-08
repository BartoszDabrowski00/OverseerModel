import logging
from typing import Optional

from bson import ObjectId
from pymongo import MongoClient as Client
from retry import retry

from overseer.utils.config.config import Config

log = logging.getLogger(__name__)


class MongoClient:
    config = Config()
    client: Optional[Client] = None
    connection_string = config.get('mongo', 'connection_string')
    username = config.get('mongo', 'username')
    password = config.get('mongo', 'password')
    overseer_db = config.get('mongo', 'overseer_db')
    overseer_recordings_collection = config.get('mongo', 'overseer_recordings_collection')

    @classmethod
    @retry(tries=3, delay=1)
    def connect(cls):
        log.info(f'Connecting to mongo')
        cls.client = Client(cls.connection_string, username=cls.username, password=cls.password)

    @classmethod
    def get_recording(cls, id):
        if not cls.client:
            cls.connect()

        log.info(f'Looking for recording with id {id}')
        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)
        result = collection.find_one({'_id': ObjectId(id)},
                                     {'recording': 1, '_id': 0})

        return result.get('recording', None)

    @classmethod
    def update_recording_with_features(cls, document_id, emotions_distribution):
        if not cls.client:
            cls.connect()

        log.info(f'Updating recording {document_id} with features')
        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)
        collection.update_one({
            '_id': ObjectId(document_id)
        }, {
            '$set': {
                'features': emotions_distribution
            }

        })
