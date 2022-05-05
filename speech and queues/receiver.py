#!/usr/bin/env python
import pika
import time
from speechText import speechToText

#create pika connection at the local host
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

#create channel
channel = connection.channel()

#create queue as task queue
#durable means task will be saved even if it does not make it
channel.queue_declare(queue='task_queue', durable=True)
#notify that receiver is ready
print('Waiting for messages to queue. CTRL+C will exit')

#when message received notify and run speechToText function
def callback(ch, method, properties, body):
    print("Received %r" % body.decode())
    speechToText(body)
    print("Job Done")

    #acknowledgement of delivery for producer
    ch.basic_ack(delivery_tag=method.delivery_tag)

#allowed to prefetch 1 task
channel.basic_qos(prefetch_count=1)
#use up that task in the queue
channel.basic_consume(queue='task_queue', on_message_callback=callback)

#take task
channel.start_consuming()
