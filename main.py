import libs.rabbit as rabbit
from datetime import datetime
import json

_user = 'Damian'

rabbitMQ = rabbit.RabbitSender()

def write():
    return input("\n~# ")

def compile(user, message):
    time = datetime.today()
    packet = {
        'time': str(time),
        'user': user,
        'message': message
    }
    return packet

try:
    rabbitMQ.connect()
    try:
        while True:
            try:
                msg = write()
            except KeyboardInterrupt:
                print('\n')
                rabbitMQ.close()
                break
            ready = compile(_user, msg)
            if msg != 'exit':
                rabbitMQ.send(ready)
            else:
                rabbitMQ.close()
                break
    except Exception as e:
        rabbitMQ.close()
        print(f'[!] Connection closed => ERROR ==> {str(e)}')
            
except Exception as e:
    print(f'[!] ERROR ==> {str(e)}')