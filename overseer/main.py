import logging
from overseer.recordings_processor import RecordingsProcessor
from overseer.utils.config.config import Config

log = logging.getLogger(__name__)


def main():
    cfg = Config()
    processor = RecordingsProcessor(cfg)
    processor.process_messages()


if __name__ == '__main__':
    log.info('Starting overseer model')
    main()
