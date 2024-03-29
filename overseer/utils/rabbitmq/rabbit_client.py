import logging
import os

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from retry import retry

from overseer.utils.config.config import Config

log = logging.getLogger(__name__)


class RabbitClient:
    config = Config()

    def __init__(self) -> None:
        self.connection = self.connect_to_rabbti()
        self.recordings_exchange = self.config.get("amqp", "recordings_exchange")
        self.recordings_exchange_type = self.config.get("amqp", "recordings_exchange_type")
        self.recordings_route = self.config.get("amqp", "recordings_route")
        self.recordings_new_queue = self.config.get("amqp", "recordings_new_queue")
        self.recordings_new_queue_type = self.config.get("amqp", "recordings_new_queue_type")
        self.channel = self.connection.channel()

        self.declare_amqp()

    @retry(tries=5, delay=2)
    def connect_to_rabbti(self):
        host = os.getenv("RABBIT_HOST", self.config.get("amqp", "host"))
        log.info(f'Connecting to rabbit on host {host}')

        return BlockingConnection(ConnectionParameters(
            host=host,
            port=self.config.get("amqp", "port"),
            virtual_host=self.config.get("amqp", "vhost"),
            credentials=PlainCredentials(self.config.get("amqp", "username"), self.config.get("amqp", "password"))
        ))

    def declare_amqp(self) -> None:
        log.info(f'Declaring exchange {self.recordings_exchange}')
        self.channel.exchange_declare(exchange=self.recordings_exchange,
                                      durable=True,
                                      exchange_type=self.recordings_exchange_type)

        log.info(f'Declaring queue {self.recordings_new_queue} with type {self.recordings_new_queue_type}')
        self.channel.queue_declare(queue=self.recordings_new_queue, durable=True,
                                   arguments={'x-queue-type': self.recordings_new_queue_type})

        log.info(
            f'Binding queue {self.recordings_new_queue} to exchange {self.recordings_exchange} with routing key {self.recordings_route}')
        self.channel.queue_bind(self.recordings_new_queue, self.recordings_exchange, routing_key=self.recordings_route)
