from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer
from .config import delivery_report, schema_str
import os

from ..utils.logger import get_logger

logger = get_logger(__name__)


async def to_kafka(topic, key, value, mapper):

    schema_registry_conf = {'url': os.getenv("SCHEMA_REGISTRY_URL")}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    json_serializer = JSONSerializer(schema_str, schema_registry_client, mapper)

    producer_conf = {'bootstrap.servers': os.getenv("BOOTSTRAP_SERVERS"),
                     'key.serializer': StringSerializer('utf_8'),
                     'value.serializer': json_serializer}

    producer = SerializingProducer(producer_conf)

    logger.info("producing cheque record to topic {}".format(topic))

    producer.poll(0.0)

    try:
        producer.produce(topic=topic, key=key, value=value, on_delivery=delivery_report)

    except Exception as e:
        raise e

    logger.info("flushing records...")
    producer.flush()
