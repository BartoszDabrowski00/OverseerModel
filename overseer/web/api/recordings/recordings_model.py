from flask_restx import fields, Namespace

recordings_namespace = Namespace('Recordings', description='Endpoints handling requests with call recordings')

record_send_model = recordings_namespace.model('Record', {
    'Result': fields.String(readonly=True, description='Information whether file was uploaded successfully'),
    'TaskId': fields.String(readonly=True, description='Celery task id')
})
