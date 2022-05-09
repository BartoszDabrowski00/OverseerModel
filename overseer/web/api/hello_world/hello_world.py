import logging

from flask_restx import Resource

from overseer.web.api.hello_world.hello_world_model import hello_world_namespace, model

log = logging.getLogger(__name__)


@hello_world_namespace.route('/')
class HelloWorld(Resource):

    @hello_world_namespace.marshal_with(model)
    def get(self, name) -> dict:
        """Hello world message endpoint"""

        return {'msg': f'Hello {name}'}
