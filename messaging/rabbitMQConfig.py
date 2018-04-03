import pika, sys


def getDefaultChannel():
    credentials = pika.PlainCredentials("guest", "guest")
    conn_params = pika.ConnectionParameters(
        "localhost", credentials=credentials)
    conn_broker = pika.BlockingConnection(conn_params)
    channel = conn_broker.channel()
    return channel