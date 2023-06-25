import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
# Enables publish confirms
channel.confirm_delivery()

# Enables transactions
channel.tx_select()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# Creates a durable queue that survives restarts
channel.queue_declare(queue='letterbox', durable=True)

message = "Hello this is my first message"

channel.basic_publish(
    exchange='pubsub',
    routing_key='',
    body=message,
    # Set properties including custom headers, delivery mode (message persistance),
    # expiration and content_type
    properties=pika.BasicProperties(
        headers = {'name': 'brain'},
        delivery_mode=1,
        expiration=13434343,
        content_type="application/json"
    ),
    # Set the publish to be mandatory - i.e. receive a notification of failure
    mandatory=True
)

# Commit a transaction
channel.tx_commit()

# Rollback a transaction
channel.tx_rollback()

print(f"sent message: {message}")

connection.close()
