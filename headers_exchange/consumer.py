import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
    print(f'received new message: {body}')

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="headers", exchange_type=ExchangeType.headers)

queue = channel.queue_declare(queue='', exclusive=True)

bind_args = {
    "x-match": "all",
    "name": "brian",
    "age": "53"
}

channel.queue_bind(queue=queue.method.queue, exchange="headers", arguments=bind_args)

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Started consuming')

channel.start_consuming()
