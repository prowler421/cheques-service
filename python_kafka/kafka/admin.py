from confluent_kafka.admin import AdminClient, NewTopic
from ..data import banks_dict
import os

from ..utils.logger import get_logger

logger = get_logger(__name__)


async def create_kafka_topics():

    logger.info("creating new kafka topics...")

    admin_client = AdminClient({
        "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS")
    })

    topics = []

    for bank_id in banks_dict.keys():
        topics.append(
            NewTopic(topic=str(bank_id) + '.funds.cheques.clearinghouse', num_partitions=3, replication_factor=1))
        topics.append(
            NewTopic(topic=str(bank_id) + '.funds.cheques.stales', num_partitions=3, replication_factor=1))
        topics.append(
            NewTopic(topic=str(bank_id) + '.funds.cheques.postdated', num_partitions=3, replication_factor=1))

    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    fs = admin_client.create_topics(topics)

    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logger.info("Topic {} created".format(topic))
        except Exception as e:
            logger.error("Failed to create topic {}: {}".format(topic, e))
