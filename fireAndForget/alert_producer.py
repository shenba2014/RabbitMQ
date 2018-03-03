import json, pika
from optparse import OptionParser

opt_parser = OptionParser()
opt_parser.add_option(
    "-r",
    "--routing-key",
    dest="routing_key",
    help="Routing key for message (e.g. myalert.im)")

opt_parser.add_option(
    "-m", "--message", dest="message", help="Message text for alert.")

args = opt_parser.parse_args()[0]

AMQP_SERVER = "localhost"
AMQP_USER = "alert_user"
AMQP_PASS = "alertme"
AMQP_VHOST = "/"
AMQP_EXCHANGE = "alerts"

creds_broker = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
conn_params = pika.ConnectionParameters(
    AMQP_SERVER, virtual_host=AMQP_VHOST, credentials=creds_broker)
conn_broker = pika.BlockingConnection(conn_params)
channel = conn_broker.channel()

msg = json.dumps(args.message)
msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"
msg_props.durable = False

channel.basic_publish(
    body=msg,
    exchange=AMQP_EXCHANGE,
    properties=msg_props,
    routing_key=args.routing_key)

print("Sent message %s tagged with routing key '%s' to exchange '/'.") % (
    json.dumps(args.message), args.routing_key)
