import time
import zmq

ctx = zmq.Context.instance()

url = "tcp://127.0.0.1:5555"

for i in range(10):
    client = ctx.socket(zmq.REQ)
    client.connect(url)
    client.send(b"request %i" % i)
    reply = client.recv_string()
    print("client recvd %r" % reply)
    time.sleep(0.1)
    client.close()

ctx.term()
