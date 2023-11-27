from flask import Flask, render_template
from flask_sockets import Sockets
from twilio.twiml.voice_response import VoiceResponse, Start
import json
import base64


HTTP_SERVER_PORT = 8080

app = Flask(__name__)
sockets = Sockets(app)

def log(msg, *args):
    print(f"Media WS: ", msg, *args)


@app.route('/twiml', methods=['POST'])
def return_twiml():
    print("POST TwiML")
    

    response = VoiceResponse()
    start = Start()
    start.stream(
        name='Example Audio Stream', url='https://call-dt8b.onrender.com/'
    )
    response.append(start)
    
    print(response)

@sockets.route('/')
def echo(ws):
    priint("Connection accepted")
    count = 0
    has_seen_media = False
    while not ws.closed:
        message = ws.receive()
        if message is None:
            log("No message received...")
            continue

        data = json.loads(message)
        if data['event'] == "connected":
            print("Connected Message received", message)
        if data['event'] == "start":
            print("Start Message received", message)
        if data['event'] == "media":
            if not has_seen_media:
                print("Media message", message)
                prinnt("Additional media messages from WebSocket are being suppressed....")
                has_seen_media = True
        if data['event'] == "closed":
            print("Closed Message received", message)
            break
        count += 1

    print("Connection closed. Received a total of {} messages".format(count))


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', HTTP_SERVER_PORT), app, handler_class=WebSocketHandler)
    print("Server listening on: http://localhost:" + str(HTTP_SERVER_PORT))
    server.serve_forever()
