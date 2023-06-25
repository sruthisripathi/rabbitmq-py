import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="first", exchange_type=ExchangeType.direct)

channel.exchange_declare(exchange="second", exchange_type=ExchangeType.fanout)

channel.exchange_bind(destination="second", source="first", routing_key="green")

message = "This message has gone through multiple exchanges"

channel.basic_publish(exchange='first', routing_key='green', body=message)

print(f"sent message: {message}")

message = "This message has gone through a single exchange"

channel.basic_publish(exchange='first', routing_key='blue', body=message)

print(f"sent message: {message}")

connection.close()
