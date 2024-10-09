import pika, json


def upload(f, fs, channel, access):
    try:
        print("uploading file to mongodb...")
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error(file upload unsuccesful)", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        if not channel.is_open:
            print("RabbitMQ channel is closed. Reconnecting...")
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq", heartbeat=600))
            channel = connection.channel()
        
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print('Message published to the queue')

    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error (failed to push to queue)", 500