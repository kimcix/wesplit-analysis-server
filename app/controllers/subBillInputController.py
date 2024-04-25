import pika
import json
from app.models.subBillModel import *
from app.db import DATABASE

def consume():
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='localhost'))
    rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')
    rabbitmq_parameters = pika.ConnectionParameters('192.168.0.225', 5672, '/', rabbitmq_credentials)    
    connection = pika.BlockingConnection(rabbitmq_parameters)
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

        #save_to_database
        """
        Message example (4/24/2024):
        master_bill_creation: {'masterBillName': 'Split Bill',
                               'masterBillId': '6629f4aca4b8026d9fe37e28',
                               'creator': 'leoren',
                               'createAt': '2024-04-24T23:14:04.448116',
                               'assignedTo': '123', 'value': 33.33}
        """
        newSubBill = SubBill(msg['masterBillId'], msg['masterBillName'], msg['assignedTo'], msg['creator'], msg['createAt'],[], msg['value'])
        newSubBill.setAnalytics()
        newSubBill.insertSubBill(DATABASE)
        # publish to subscribers

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming()

    return