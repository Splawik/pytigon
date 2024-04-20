import zmq

var responder = zmq.listen("tcp://127.0.0.1:5555", REP)
for i in 0..10:
    var request = receive(responder)
    echo("Received: ", request)
    send(responder, "World")
close(responder)
