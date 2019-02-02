from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

app.debug = True
app.secret_key = 'development key'

socketio = SocketIO(app)

@app.route('/',methods=['GET'])
def hellopage():
    return render_template('hello.html')

@app.route('/messages',methods=['POST'])
def messagespage():
    name = request.form['username']
    message = request.form['message']
    return "Message : " + message + " received" + " for user : " + name

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

"""
@app.route('/test1', methods=['GET'])
def test1():
    value = request.sid
    return "My id is :" + value
"""

if __name__ == "__main__":
    socketio.run(app)
