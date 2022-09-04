from overseer.utils.config.config import Config
from overseer.utils.mongo.mongo_client import MongoClient
from overseer.utils.rabbitmq.rabbit_client import RabbitClient


def main():
    cfg = Config()
    mongo_client = MongoClient()
    rabbit_client = RabbitClient()


if __name__ == '__main__':
    main()
