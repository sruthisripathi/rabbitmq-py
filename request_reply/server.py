import pika

def on_request_message_received(channel, method, properties, body):
    print(f'Received request: {properties.correlation_id}')
    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        body=f'Hey, its your reply to {properties.correlation_id}'
    )

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='request-queue')

channel.basic_consume(queue='request-queue', auto_ack=True, on_message_callback=on_request_message_received)

print('Starting server')

channel.start_consuming()
