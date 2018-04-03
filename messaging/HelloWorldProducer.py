import sys
import pika
import rabbitMQConfig

channel = rabbitMQConfig.getDefaultChannel()

channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"

channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola")
