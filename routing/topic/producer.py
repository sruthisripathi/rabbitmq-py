import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

european_payment_message = "A european user paid for something"
channel.basic_publish(exchange='topic', routing_key='user.europe.payments', body=european_payment_message)
print(f"sent message: {european_payment_message}")

business_order_message = "A european business ordered goods"
channel.basic_publish(exchange='topic', routing_key='business.europe.order', body=business_order_message)
print(f"sent message: {business_order_message}")

indian_user_order = "An indian user ordered goods"
channel.basic_publish(exchange='topic', routing_key='user.india.order', body=indian_user_order)
print(f"sent message: {indian_user_order}")

connection.close()
