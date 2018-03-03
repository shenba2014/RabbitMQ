<?php
require_once './php-amqplib/amqp.inc';
require_once 'config.php';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();
list($errors_queue) = $channel->queue_declare();
list($warnings_queue) = $channel->queue_declare();
list($info_queue) = $channel->queue_declare();

$exchange = 'amq.rabbitmq.log';

$channel->queue_bind($errors_queue, $exchange, "error");
$channel->queue_bind($warnings_queue, $exchange, "warning");
$channel->queue_bind($info_queue, $exchange, "info");

$error_callback = function ($msg) {
    echo 'error: ', $msg->body, "\n";
    $msg->delivery_info['channel']->basic_ack(
        $msg->delivery_info['delivery_tag']
    );
};

$warning_callback = function ($msg) {
    echo 'warning: ', $msg->body, "\n";
    $msg->delivery_info['channel']->basic_ack(
        $msg->delivery_info['delivery_tag']
    );
};

$info_callback = function ($msg) {
    echo 'info: ', $msg->body, "\n";
    $msg->delivery_info['channel']->basic_ack(
        $msg->delivery_info['delivery_tag']
    );
};

$channel->basic_consume($errors_queue, "", false, false, false, false, $error_callback);
$channel->basic_consume($warnings_queue, "", false, false, false, false, $warning_callback);
$channel->basic_consume($info_queue, "", false, false, false, false, $info_callback);

while (count($channel->callbacks)) {
    $channel->wait();
}
