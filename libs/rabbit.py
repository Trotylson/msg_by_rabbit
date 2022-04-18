import os
import pika
import sys
import time
import libs.configParser as configParser
from datetime import datetime
import json

config = configParser.ConfigParser()
config.read('config/config.ini')

"""
[!] ERROR ==> credentials must be an object of type: [<class 'pika.credentials.PlainCredentials'>, <class 'pika.credentials.ExternalCredentials'>], but got ('admin', 'admin')
"""

class RabbitSender:
    
    def __init__(self):
        self._host = config.get('rabbit', 'host')
        self._port = config.get('rabbit', 'port')
        self._exchange = config.get('rabbit', 'exchange')
        self._rKey = config.get('rabbit', 'rKey')
        self.v_host = config.get('rabbit', 'vHost')
        self.credentials = pika.PlainCredentials(username=config.get('rabbit', 'login'), password=config.get('rabbit', 'password'))
    
    def connect(self):
        print(f'[?] Trying connect to Rabbit {self._host} : {self._port}')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host, 
                                                                            port=self._port, 
                                                                            virtual_host=self.v_host,
                                                                            credentials=self.credentials))
        self.channel = self.connection.channel()
        print(f'[OK] Connected!')

    def send(self, msg):
        self.channel.basic_publish(exchange=self._exchange,
                            routing_key=self._rKey, 
                            body=json.dumps(msg))
        print(f"[{datetime.today()}] sent to ==> {self._host}: {self._port}")
        

    def close(self):
        self.connection.close()
        print(f'[BYE] Connection with SERVER {self._host}:{self._port} closed successfully!')
        

    


   
    