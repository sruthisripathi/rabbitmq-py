import pika

def on_message1_received(channel, method, properties, body):
    print(f'queue 1 received new message: {body}')

def on_message2_received(channel, method, properties, body):
    print(f'queue 2 received new message: {body}')

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.exchange_declare(exchange="hashing", exchange_type="x-consistent-hash")

channel.queue_declare(queue='letterbox1')
channel.queue_declare(queue='letterbox2')

channel.queue_bind(queue='letterbox1', exchange="hashing", routing_key='1')
channel.basic_consume(queue='letterbox1', auto_ack=True, on_message_callback=on_message1_received)

channel.queue_bind(queue='letterbox2', exchange="hashing", routing_key='3')
channel.basic_consume(queue='letterbox2', auto_ack=True, on_message_callback=on_message2_received)


print('Started consuming')

channel.start_consuming()
