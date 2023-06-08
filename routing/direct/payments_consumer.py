import pika
from pika.exchange_type import ExchangeType

def on_message_received(channel, method, properties, body):
    print(f'Payments service - received new message: {body}')

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='direct', exchange_type=ExchangeType.direct)

queue = channel.queue_declare(queue='', exclusive=True) # exclusive true makes this a temporary queue

channel.queue_bind(queue=queue.method.queue, exchange='direct', routing_key='paymentsonly')
# channel.queue_bind(queue=queue.method.queue, exchange='direct', routing_key='analyticsonly')
# routing_key can be changed to say, analyticsonly to accept messages for analytics service
# or a second binding can also be added

channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

print('Started consuming')

channel.start_consuming()
