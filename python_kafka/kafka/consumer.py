from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import StringDeserializer

from python_kafka.model.mappers import dict_to_check, check_to_dict
from .config import schema_str
import os
from typing import Dict, Callable

from .producer import to_kafka
from ..model.cheque import Cheque
from ..services.cheques_service import is_cheque_stable
from ..data import banks_dict
from ..utils.logger import get_logger

logger = get_logger(logname=__name__)


async def process_clearinghouse(cheque: Cheque):

    logger.info('processing new cheque in clearinghouse')

    is_stable = is_cheque_stable(cheque)
    topic = f'{cheque.bk_sender_id}.funds.cheques.stales' if is_stable else f'{cheque.bk_sender_id}.funds.cheques.postdated'

    logger.info('cheque validity: {0} - pushing message to topic: {1}'.format(is_stable, topic))
    await to_kafka(topic=topic, key=cheque.issuer_account_id, value=cheque, mapper=check_to_dict)


async def process_stales(cheque: Cheque):
    logger.info('processing stale cheque: {0}'.format(cheque))
    banks_dict[cheque.bk_sender_id].bank_accounts[cheque.issuer_account_id] += cheque.chk_amount
    banks_dict[cheque.bk_receiver_id].bank_accounts[cheque.issued_account_id] -= cheque.chk_amount


async def process_postdated(cheque: Cheque):
    logger.info('cheque has been marked as postdated {0}'.format(cheque))


topics_dict: Dict[str, Callable] = {}

for bank_id in banks_dict:
    topics_dict[str(bank_id) + '.funds.cheques.clearinghouse'] = process_clearinghouse
    topics_dict[str(bank_id) + '.funds.cheques.stales'] = process_stales
    topics_dict[str(bank_id) + '.funds.cheques.postdated'] = process_postdated


async def from_kafka():
    print("Initializing kafka consumer...")
    json_deserializer = JSONDeserializer(schema_str,
                                         from_dict=dict_to_check)
    string_deserializer = StringDeserializer('utf_8')

    consumer_conf = {'bootstrap.servers': os.getenv("BOOTSTRAP_SERVERS"),
                     'key.deserializer': string_deserializer,
                     'value.deserializer': json_deserializer,
                     'group.id': 1,
                     'auto.offset.reset': "earliest"}

    consumer = DeserializingConsumer(consumer_conf)
    consumer.subscribe(list(topics_dict.keys()))

    while True:
        try:

            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            cheque = msg.value()

            if cheque is not None:
                logger.info('pulled new message from {0}'.format(msg.topic().__str__()))
                logger.info('object {0}: {1}'.format(type(cheque), cheque))
                await topics_dict[msg.topic()](cheque)
        except KeyboardInterrupt as e:
            print(e)

    consumer.close()
