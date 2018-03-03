<?php
include_once './php-amqplib/amqp.inc';
include_once 'rabbitmq-config.php';

$conn = new AMQPConnection(HOST, PORT, USER, PASS);
$channel = $conn->channel();

$channel->exchange_declare('upload-pictures', 'fanout', false, true, false);

if ($argv[1] == 'quit') {
    $channel->basic_publish(
        new AMQPMessage('quit', array('content_type' => 'html/text', 'delivery_mode' => 2))
        , 'upload-pictures');
} else {
    $image_id = $argv[1];
    $user_id = $argv[2];
    $image_path = $argv[3];
    $metadata = json_encode(array('image_id' => $image_id, 'user_id' => $user_id, 'image_path' => $image_path));

    $msg = new AMQPMessage($metadata, array('content_type' => 'application/json', 'delivery_mode' => 2));

    $channel->basic_publish($msg, 'upload-pictures');
}

$channel->close();
$conn->close();
