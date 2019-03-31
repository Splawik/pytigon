# -*- coding: utf-8 -*-
import urllib
import copy

SCOPE_TEMPLATE = {
    'type': 'http',
    'http_version': '1.1',
    'method': 'GET',
    'path': '/',
    'root_path': '',
    'scheme': 'http',
    'query_string': b'',
    'headers': [
        (b'host', b'127.0.0.2'),
        (b'user-agent', b'python-urllib3/0.6 asgi bridge'),
        (b'accept', b'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        (b'accept-language', b'pl,en-US;q=0.7,en;q=0.3'),
        (b'accept-encoding', b'gzip, deflate'),
        (b'origin', b'http://127.0.0.2'),
        (b'connection', b'keep-alive'),
        (b'cache-control', b'max-age=0')
    ],
    'client': ['127.0.0.2', 60748],
    'server': ['127.0.0.2', 80]
}

def get_scope_and_content_http_get(path, headers):
    scope = copy.deepcopy(SCOPE_TEMPLATE)
    if '?' in path:
        x = path.split('?', 1)
        path2 = x[0]
        query = x[1]
    else:
        path2 = path
        query = ""

    scope['path'] = path2
    scope['query_string'] = query.encode('utf-8')
    for pos in headers:
        if type(pos[0]) == str:
            key = pos[0].encode('utf-8')
        else:
            key = pos[0]
        for pos2 in scope['headers']:
            if type(pos2[0]) == str:
                key2 = pos2[0].encode('utf-8')
            else:
                key2 = pos2[0]

            if key.lower() == key2.lower():
                scope['headers'].remove(pos2)
                break
        scope['headers'].append((key, pos[1]))

    return scope, ""


def get_scope_and_content_http_post(path, headers, params={}):
    scope, content = get_scope_and_content_http_get(path, headers)
    scope['method'] = 'POST'
    scope['headers'].append((b'upgrade-insecure-requests', b'1'))
    scope['headers'].append((b'content-type', b'application/x-www-form-urlencoded'))
    if params:
        content = urllib.parse.urlencode(params)
    else:
        content = ""
    scope['headers'].append((b'content-length', str(len(content)).encode('utf-8') ))
    return scope, content


def get_scope_websocket(path, headers):
    scope, content  = get_scope_and_content_http_get(path, headers)
    scope['type'] = 'websocket'
    return scope


async def get_or_post(application, path, headers, params={}, post=False):
    ret = {}
    if post:
        scope, content = get_scope_and_content_http_post(path, headers, params)
    else:
        scope, content = get_scope_and_content_http_get(path, headers)
    async def send(message):
        nonlocal ret
        for key, value in message.items():
            ret[key] = value

    async def receive():
        nonlocal content
        return {'type': 'http', 'body': content.encode('utf-8')}

    app_instance = application(scope)
    application_queue = await app_instance(receive, send)

    if 'status' in ret and ret['status'] == 302:
        if 'headers' in ret:
            for pos in ret['headers']:
                if pos[0] == b'Location':
                    new_url = pos[1].decode('utf-8').replace('http://127.0.0.2', '')
                    ret2 = await get_or_post(application, new_url, headers)
                    if 'headers' in ret:
                        for pos2 in ret['headers']:
                            ret2['headers'].append(pos2)
                    return ret2

    return ret


async def websocket(application, path, headers, input_queue, output):
    ret = {}
    status = 0
    scope = get_scope_websocket(path.replace('ws://127.0.0.2/', ''), headers)

    async def send(message):
        nonlocal output
        if 'type' in message:
            if message['type'] == 'websocket.accept':
                output.onOpen()
            elif message['type'] == 'websocket.send':
                text = None
                binary = None
                if 'text' in message:
                    text = message['text']
                if 'binary' in message:
                    binary = message['binary']
                output.onMessage(text, binary)
            elif message['type'] == 'websocket.disconnect':
                output.onClose(None, None, None)

    async def receive():
        nonlocal status
        nonlocal input_queue
        item = await input_queue.get()
        if item:
            return {'type': 'websocket.receive', 'text': item}
        else:
            return {'type': 'websocket.disconnect'}

    app_instance = application(scope)
    application_queue = await app_instance(receive, send)

    return ret
