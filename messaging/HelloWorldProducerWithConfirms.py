import pika
from pika import spec
import sys
import rabitconfig

channel = rabitconfig.getDefaultChannel()

msg_ids = []


def confirm_handler(frame):
    if type(frame.method) == spec.Confirm.SelectOk:
        print "Channel in 'confirm' mode."
    elif type(frame.method) == spec.Basic.Nack:
        if (frame.method.delivery_tag in msg_ids):
            print "Message lost!"
    elif type(frame.method) == spec.Basic.Ack:
        if (frame.method.delivery_tag in msg_ids):
            print "Confirm received!"
            msg_ids.remove(frame.method.delivery_tag)


channel.confirm_delivery()

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
channel.basic_publish(
    body=msg,
    exchange="hello-exchange",
    properties=msg_props,
    routing_key="hola")
msg_ids.append(len(msg_ids) + 1)
channel.close()
