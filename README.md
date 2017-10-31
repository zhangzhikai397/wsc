# WebSocket Channel

WebSocket Channel is a Python3 lightweight and very fast server, to be used to communicate any python
backend with users browsers via WebSockets protocol. WebSocket Channel has very simple API and can work only
in one direction - `server -> browser`. Any browser's messages that was sent to the server.
will be ignored.

**Channel** - it's an server endpoint like http://0.0.0.0:8088`/user1/`. Browsers can subscribe to this
 endpoint using JS WebSockets to get messages from server. Or you can send `POST` request to this endpoint
 to send message for each channel subscriber.

**Requirements**

 - Python 3.4 or higher
 - Python PIP

# Installation

**shell**

    pip install wsc
    
# Run server

Command `wsc` has only three arguments and one of them is required.

 - ACCESS_KEY (required, positional): It's any string to be used to avoid unexpected access to websocket serving API.
 - --host (optional, 0.0.0.0): Server host
 - --port (optional, 8088): Server port

**shell**

    $ wsc A0B1C2D3 --host 0.0.0.0 --port 8080
    
# Send message to user's browser

To send messages to browsers, WebSocket Channel has special simple HTTP API. For example,
you can send POST Request to any endpoint with configured access key, then request body will
be served to all channel subscribers.

**python**

    import requests
    
    # This simple example will send message "Admin: Hi all" to
    # all browsers that are subscribed to channel "/chat/room/1"
    endpoint = 'http://0.0.0.0:8080/chat/room/1'    
    requests.post(endpoint, headers={'access-key': 'A0B1C2D3'}, data='Admin: Hi all')


Client library usage

**python**

    from wsc.client import WSC
    
    # The same result using client library
    c = WSC('A0B1C2D3', '0.0.0.0', 8080)
    c.send('chat/room/1', 'Admin: Hi all')
    
    
# Receiving messages

To receive message from websocket server on client side, you should do something like this

**javascript**

    window.ws = new WebSocket('ws://127.0.0.1:8080/chat/room/1');
    ws.onclose = function () {
        console.error('Connection closed');
    };

    ws.onerror = function () {
        console.error('Error happened');
    };

    ws.onmessage = function (msg) {
        console.log('Received', msg.data);
    };
    
Also, you can see simple example at `test.html` file