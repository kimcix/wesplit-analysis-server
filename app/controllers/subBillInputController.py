import pika
import json

def consume():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='sda_mq', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # TODO: Change the routing_key below
    channel.queue_bind(exchange='sda_mq', queue=queue_name, routing_key='master_bill_creation')

    print(f" [x] Consumer starts listening....")


    def callback(ch, method, properties, body):
        msg = json.loads(body)
        print(f" [x] {method.routing_key}: {msg}")

        # publish to subscribers

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()