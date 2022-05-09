import logging

from celery import Celery
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

import overseer.web.celery as celery_cfg
from overseer.web.api.recordings.recordings_model import record_send_model, recordings_namespace

log = logging.getLogger(__name__)

upload_parser = recordings_namespace.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@recordings_namespace.route('/')
class Recordings(Resource):
    PROCESS_SIGNAL_TASK_NAME = 'process_signal'
    PROCESS_SIGNAL_QUEUE = 'process_signal_queue'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.celery = Celery()
        self.celery.config_from_object(celery_cfg)

    @recordings_namespace.marshal_with(record_send_model)
    def post(self) -> dict:
        """Recording receiving endpoint"""

        log.info('Got recording send request')
        args = upload_parser.parse_args()
        uploaded_file = args.get('file')
        if not uploaded_file and self._validate_file(uploaded_file):
            log.error('File didnt pass validation. Request aborted')
            return {'result': 'failed'}

        serialized_file = self._serialize_file(uploaded_file)
        task_id = self.celery.send_task(self.PROCESS_SIGNAL_TASK_NAME,
                                        ([serialized_file]),
                                        queue=self.PROCESS_SIGNAL_QUEUE
                                        )

        log.info(f'Recording accepted. Celery task id: {task_id}')
        return {'result': 'Successful', 'taskId': task_id}

    def _validate_file(self, uploaded_file: FileStorage):
        return 'audio' not in uploaded_file.mimetype

    def _serialize_file(self, uploaded_file):
        # TODO("SERIALIZE")
        raise NotImplemented()
