import rabitconfig
import pika

channel = rabitconfig.getDefaultChangel()

channel.exchange_declare(
    exchange="hello-exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)

channel.queue_declare(queue="hello-queue")
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