import BlockingConnection
import pika
import rabbitMQConfig

channel = rabbitMQConfig.getDefaultChannel()

channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)

# here is the difference for mirrored queue
queue_args = {"x-ha-policy": "all"}
channel.queue_declare(queue="hello-queue", arguments=queue_args)
channel.queue_bind(
    queue="hello-queue", exchange="hello-exchange", routing_key="hola")


def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print body

    return


channel.basic_consume(
    msg_consumer, queue="hello-queue", consumer_tag="hello-consumer")
channel.start_consuming()