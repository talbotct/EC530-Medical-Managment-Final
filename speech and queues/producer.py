#!/usr/bin/env python
import pika
import sys

#create pika connection at the local host
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

#create channel
channel = connection.channel()

#create queue as task queue
#durable means task will be saved even if it does not make it
channel.queue_declare(queue = 'task_queue', durable = True)

#input for audio file name or link
audioSource = ' '.join(sys.argv[1:])

#publish the task as a message for the receiver
channel.basic_publish(exchange = '', routing_key = 'task_queue', body = audioSource, properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE))

#confirm the task was sent
print("Sent %r" % audioSource)

#close connection
connection.close()
