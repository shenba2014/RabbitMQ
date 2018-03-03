<?php
require_once './php-amqplib/amqp.inc';
require_once 'rabbitmq-config.php';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();

$channel->exchange_declare('upload-pictures', 'fanout', false, true, false);

list($queue) = $channel->queue_declare('add-points', false, true, false, false);

$channel->queue_bind('add-points', 'upload-pictures');

$consumer = function ($msg) {
    if ($msg->body == 'quit') {
        $msg->delivery_info['channel']->basic_cancel($msg->delivery_info['consumer_tag']);
        echo "server quit....\n";
    }
    
    $meta = json_decode($msg->body, true);
    $user_id = $meta['user_id'];
    echo sprintf("Adding points to user: %s\n", $user_id);
    $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);

};

$channel->basic_consume('add-points', "upload-pictures", false, false, false, false, $consumer);

while (count($channel->callbacks)) {
    $channel->wait();
}

$channel->close();
$conn->close();
