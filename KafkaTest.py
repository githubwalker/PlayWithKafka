#!/usr/bin/python3.6
# https://kafka-python.readthedocs.io/en/master/usage.html
# https://forums.docker.com/t/connecting-kafka-producer-to-kafka-broker-in-docker-through-java/85272

import json
import signal
import sys
import time

import kafka
import argparse
import enum
import typing


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!. Leaving...')
    sys.exit(0)


class ConsumerProducer(enum.Enum):
    PRODUCER = 'p'
    CONSUMER = 'c'

    def __init__(self, strVal):
        self.val = strVal


class Params(typing.NamedTuple):
    cp: ConsumerProducer
    addr: str
    topic: str


def parse_args():
    parser = argparse.ArgumentParser(description='kafka example test')

    parser.add_argument('--cp', help='producer(p) or consumer(c)', required=True)
    parser.add_argument('--addr', help='kafka addr:port', required=True)
    parser.add_argument('--topic', help='kafka topic', required=True)

    args = parser.parse_args()
    return Params(cp=ConsumerProducer(args.cp), addr=args.addr, topic=args.topic)


def entry_point():
    params = parse_args()

    if params.cp == ConsumerProducer.PRODUCER:
        producer = kafka.KafkaProducer(bootstrap_servers=[params.addr],
                                       value_serializer=lambda x:
                                       json.dumps(x).encode('utf-8'))

        while True:
            for i in range(0,sys.maxsize):
                data = {'number': i}
                producer.send(params.topic, value=data)
                time.sleep(1)
    else:
        consumer = kafka.KafkaConsumer(
            params.topic,
            bootstrap_servers=[params.addr],
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))

        for message in consumer:
            message = message.value
            print("message is %s" % message)

    pass


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    entry_point()
