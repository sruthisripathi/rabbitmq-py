import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
    print(f'Payments service - received new message: {body}')

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(queue=queue.method.queue, exchange='topic', routing_key='user.#')

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Started consuming')

channel.start_consuming()
