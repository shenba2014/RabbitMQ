import sys, json, pika, time, traceback


def msg_rcvd(channel, method, header, body):
    message = json.loads(body)
    print "Received order %(ordernum)d for %(type)s." % message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    AMQP_SERVER = sys.argv[1]
    AMQP_PORT = int(sys.argv[2])
    AMQP_USER = sys.argv[3]
    AMQP_PASSWORD = sys.argv[4]
    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
    conn_params = pika.ConnectionParameters(
        AMQP_SERVER,
        port=AMQP_PORT,
        virtual_host="/",
        credentials=creds_broker)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    print "Ready for orders!"
    channel.basic_consume(
        msg_rcvd,
        queue="shovel_income_queue",
        no_ack=False,
        consumer_tag="shovel_key")
    channel.start_consuming()