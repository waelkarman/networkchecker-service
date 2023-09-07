#
# Pathological publisher
# Sends out 1,000 topics and then one random update per second
#

import sys
import time
import socket
import fcntl
import struct
from random import randint

import zmq

def main(url=None):

    
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")

    while True:
        # Send one random update per second
        time.sleep(1)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print(s.getsockname()[0])

            # Ensure subscriber connection has time to complete
            ipstr = f"AWAKE ON {s.getsockname()[0]}"
            publisher.send_multipart([
                b"PASSIVEBUZZER",
                bytes(ipstr, 'utf-8'),
            ])
        except Exception as e:
            publisher.send_multipart([
                b"PASSIVEBUZZER",
                bytes("NOT CONNECTED", 'utf-8'),
            ])
            

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
