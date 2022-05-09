import logging

from flask_restx import Api

from overseer.web.api.hello_world.hello_world import hello_world_namespace
from overseer.web.api.recordings.recordings import recordings_namespace

log = logging.getLogger(__name__)


def register_endpoints(api: Api) -> None:
    log.info('Starting registering endpoints')

    api.add_namespace(hello_world_namespace, '/greeting/<string:name>')
    api.add_namespace(recordings_namespace, '/recordings')

    log.info('All endpoints are ready')
