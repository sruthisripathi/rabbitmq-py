import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
    print(f'received new message: {body}')

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Giving empty queue name will let the server choose a random name
# exclusive=True tells the broker to delete the queue once the connection is closed (temporary queue)
queue = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Started consuming')

channel.start_consuming()
