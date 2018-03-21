import sys, json, pika, time, traceback


def msg_rcvd(channel, method, header, body):
    message = json.loads(body)
    print "Received: %(content)s/%(time)d" % message
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    AMQP_SERVER = sys.argv[1]
    AMQP_PORT = int(sys.argv[2])
    AMQP_USER = sys.argv[3]
    AMQP_PWD = sys.argv[4]

    creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PWD)
    conn_params = pika.ConnectionParameters(
        AMQP_SERVER,
        port=AMQP_PORT,
        virtual_host="/",
        credentials=creds_broker)

    while True:
        try:
            conn_broker = pika.BlockingConnection(conn_params)
            channel = conn_broker.channel()
            channel.exchange_declare(
                exchange="cluster_test", exchange_type="direct", auto_delete=False)
            channel.queue_declare(queue="cluster_test", auto_delete=False)
            channel.queue_bind(
                queue="cluster_test",
                exchange="cluster_test",
                routing_key="cluster_test")

            print "Ready for testing!"
            channel.basic_consume(msg_rcvd, queue="cluster_test", no_ack=False, consumer_tag="cluster_test")
            channel.start_consuming()
        except Exception, e:
            traceback.print_exc()