# [json]
def on_delivery_json(err, msg):

    if err is not None:
        print('message delivery failed: {}'.format(err))
    else:
        print('message successfully produced to {} [{}] at offset {}'.format(msg.topic(), msg.partition(), msg.offset()))


# [avro]
def on_delivery_avro(err, msg, obj):

    if err is not None:
        print('message {} delivery failed for user {} with error {}'.format(obj, obj.name, err))
    else:
        print('message {} successfully produced to {} [{}] at offset {}'.format(obj, msg.topic(), msg.partition(), msg.offset()))