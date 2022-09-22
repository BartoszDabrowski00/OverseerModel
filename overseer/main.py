import logging
from overseer.recordings_processor import RecordingsProcessor
from overseer.utils.config.config import Config

log = logging.getLogger(__name__)


def main():
    cfg = Config()
    processor = RecordingsProcessor(cfg)
    processor.process_messages()


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET)
    logging.getLogger('pika').setLevel(logging.WARNING)
    log.info('Starting overseer model')
    main()
