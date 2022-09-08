import logging
import os

import toml

log = logging.getLogger(__name__)


class Config:
    CONFIG_PATH = os.getenv('OVERSEER_MODEL_CONFIG_PATH', 'config.toml')
    config = None

    @classmethod
    def get(cls, section, key):
        if cls.config is None:
            log.info(f'Loading config from {cls.CONFIG_PATH}')
            cls.config = toml.load(cls.CONFIG_PATH)

        return cls.config.get(section, {}).get(key, None)
