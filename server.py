from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.debug = True
app.secret_key = 'development key'

socketio = SocketIO(app)

list_members = []



@app.route('/',methods=['GET', 'POST'])
def hellopage():
    """
    main page of the application
    """
    return render_template('hello.html')



@socketio.on('chatmessage')
def test_message(message):
    """
    When the user send a message, the server send it to the final receiver
    """
    if message['receiver'] == 'me':
        receiver_id = request.sid
        sender_name = "me"
    else:
        receiver_id = message['receiver']
        sender_name = request.sid
    emit('follow_message', {'message':message['messagetosend'],'sender':sender_name}, room=receiver_id)


@socketio.on('connect')
def test_connect():
    """
    When a new user connect to the server, the server add his id to the list of id
    """
    list_members.append(request.sid)
    emit('send_list_members', {'data': list_members}, broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    """
    When a new user disconnect from the server, the server remove his id to the list of id
    """
    list_members.remove(request.sid)
    emit('send_list_members',  {'data': list_members}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
