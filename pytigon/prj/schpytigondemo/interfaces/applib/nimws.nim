import ws, asyncdispatch, asynchttpserver

var connections {.threadvar.}: seq[WebSocket]

proc initThread() =
  connections = newSeq[WebSocket]()

proc cb(req: Request) {.async, gcsafe.} =
  if req.url.path == "/ws":
    try:
      var ws = await newWebSocket(req)
      connections.add ws
      await ws.send("Welcome")
      while ws.readyState == Open:
        let packet = await ws.receiveStrPacket()
        echo packet
        for other in connections:
          if other.readyState == Open:
            asyncCheck other.send(packet & " from the server")
    except WebSocketError:
      echo "socket closed:", getCurrentExceptionMsg()
  else:
    await req.respond(Http404, "Not found")


initThread()
var server = newAsyncHttpServer()
waitFor server.serve(Port(9001), cb)
