from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

app.debug = True
app.secret_key = 'development key'

socketio = SocketIO(app)

list_members = []

@app.route('/',methods=['GET', 'POST'])
def hellopage():
    return render_template('hello.html')

"""
@app.route('/messages',methods=['POST'])
def messagespage():
    name = request.form['username']
    message = request.form['message']
    return "Message : " + message + " received" + " for user : " + name
"""

@socketio.on('message')
def handle_message(message):
    print(message)

@socketio.on('chatmessage')
def test_message(message):
    print("event received")
    print("receiver is " + message['receiver'])
    print("message is " + message['messagetosend'])
    
    
    if message['receiver'] == 'me':
        receiver_id = request.sid
        sender_name = "me"
    else:
        receiver_id = message['receiver']
        sender_name = request.sid
    
    
    emit('follow_message', {'message':message['messagetosend'],'sender':sender_name}, room=receiver_id)
    
    #emit('my response', {'data': message['data']})
"""
@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)
"""
@socketio.on('connect')
def test_connect():
    print("Client " + request.sid + " connected")
    #emit('my response', {'data': 'Connected'})
    list_members.append(request.sid)
    emit('send_list_members', {'data': list_members}, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    print('Client '+ request.sid +' disconnected')
    list_members.remove(request.sid)
    emit('send_list_members',  {'data': list_members}, broadcast=True)

"""
@app.route('/test1', methods=['GET'])
def test1():
    value = request.sid
    return "My id is :" + value
"""

if __name__ == "__main__":
    socketio.run(app)
