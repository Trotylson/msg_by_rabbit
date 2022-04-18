import json
import os
import pika
import sys
import time
import libs.configParser as configParser
from datetime import datetime

config = configParser.ConfigParser()
config.read('config/config.ini')


class RabbitReceiver:
    
    def __init__(self):
        self._host = config.get('rabbit', 'host')
        self._port = config.get('rabbit', 'port')
        self._queue = config.get('rabbit', 'queue')
        # self._rKey = config.get('rabbit', 'rKey')
        self.v_host = config.get('rabbit', 'vHost')
        self.credentials = pika.PlainCredentials(username=config.get('rabbit', 'login'), password=config.get('rabbit', 'password'))
    
    def main(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host, 
                                                                        port=self._port, 
                                                                        virtual_host=self.v_host,
                                                                        credentials=self.credentials))
        channel = connection.channel()

        # channel.queue_declare(queue=self._queue)

        def callback(ch, method, properties, body):
            msg = json.loads(body)
            print(f"\n.:{msg['user']}:.     {msg['time']}\n     ==> {msg['message']}")

        channel.basic_consume(queue=self._queue, on_message_callback=callback, auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

if __name__ == '__main__':
    try:
        RabbitReceiver().main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)