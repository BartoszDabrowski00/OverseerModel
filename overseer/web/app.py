import os
import logging
import toml

from flask import Flask, Blueprint
from flask_restx import Api

from overseer.web.api.endpoints import register_endpoints

CONFIG_PATH = os.getenv('CONFIG_PATH', 'overseer_config.cfg')

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1/overseer')
api = Api(blueprint)
app.register_blueprint(blueprint)


def get_cfg() -> dict:
    return toml.load(CONFIG_PATH)


def run_app() -> None:
    server_config = get_cfg().get("server", {})
    register_endpoints(api)
    app.run(port=server_config.get("port", 5000), debug=server_config.get("debug", False))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run_app()
