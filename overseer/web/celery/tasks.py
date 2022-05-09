import logging

from celery import Celery

celery = Celery()
celery.config_from_object('overseer.web.celery.celeryconfig')

log = logging.getLogger(__name__)


@celery.task(name='process_signal')
def process_signal(file):
    # TODO("PROCESS FILE")
    raise NotImplemented()
