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

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    ctx = zmq.Context.instance()
    publisher = ctx.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")
    # Ensure subscriber connection has time to complete
    time.sleep(1)

    while True:
        # Send one random update per second
        try:
            time.sleep(1)
            ipstr = f"AWAKE ON {s.getsockname()[0]}"
            publisher.send_multipart([
                b"PASSIVEBUZZER",
                bytes(ipstr, 'utf-8'),
            ])
        except KeyboardInterrupt:
            print("interrupted")
            break

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
