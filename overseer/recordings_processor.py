import logging
from io import BytesIO

from overseer.utils.mongo.mongo_client import MongoClient
from overseer.utils.rabbitmq.rabbit_client import RabbitClient
from overseer.vader_emotion_recognition.vader_classifier import VaderClassifier, TextNotConvertedException

log = logging.getLogger(__name__)


class RecordingsProcessor:
    ENCODING = 'UTF-8'

    def __init__(self, cfg):
        self.cfg = cfg
        self.mongo = MongoClient()
        self.rabbit_client = RabbitClient()
        self.vader_classifier = VaderClassifier()
        log.info('Initialized processor')

    def process_messages(self):
        self.rabbit_client.channel.basic_consume(self.rabbit_client.recordings_new_queue, self.classify)
        self.rabbit_client.channel.start_consuming()
        log.info('Starting consuming')

    def classify(self, ch, method_frame, properties, body):
        document_id = body.decode(self.ENCODING)
        log.info(f'Consuming recording with id {document_id}')
        binary_audio = BytesIO(self.mongo.get_recording(document_id))

        emotions_distribution = self.get_emotions_distribution(binary_audio)
        if not emotions_distribution:
            log.info(f'Rejecting recording with id {document_id}')
            ch.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)
            return

        self.mongo.update_recording_with_features(document_id, emotions_distribution)

        log.info(f'Successfully consumed recording with id {document_id}')
        ch.basic_ack(delivery_tag=method_frame.delivery_tag)

    def get_emotions_distribution(self, binary_audio):
        try:
            return self.vader_classifier.get_emotions_distribution(binary_audio)
        except TextNotConvertedException as e:
            log.debug(e)
            return None
