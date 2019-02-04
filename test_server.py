import json
import unittest
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from server import app, socketio

class TestServer(unittest.TestCase):
    def setUp(self):
        self.socketclient = SocketIO.test_client(socketio,app)
        self.flaskclient = app.test_client()

    def tearDown(self):
        self.socketclient.disconnect()
    
    def test_disconnect(self):
        received = self.socketclient.get_received()
        self.socketclient.disconnect()
        received = self.socketclient.get_received()
        self.assertEqual(len(received[0]['args'][0]['data']),0)

    def test_hellopage(self):
        response = self.flaskclient.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_receive_list_members(self):
        received = self.socketclient.get_received()
        self.assertEqual(received[0]['name'], 'send_list_members')
        self.assertEqual(len(received[0]['args'][0]['data']),1)
        self.assertEqual(received[0]['args'][0]['data'][0],self.socketclient.sid)
        self.assertEqual(received[0]['namespace'], '/')
        
    def test_message_myself(self):
        message = {}
        message['receiver'] = 'me'
        message['messagetosend'] = "a test message"
        self.socketclient.emit('chatmessage',message)
        received = self.socketclient.get_received()
        follow = received[1]
        self.assertEqual(follow['name'], 'follow_message')
        self.assertEqual(follow['args'][0]['message'], message['messagetosend'])
        self.assertEqual(follow['args'][0]['sender'], message['receiver'])
        self.assertEqual(follow['namespace'], '/')

    def test_message_other(self):
        newclient = SocketIO.test_client(socketio,app)
        message = {}
        message['receiver'] = newclient.sid
        message['messagetosend'] = "a test message"
        self.socketclient.emit('chatmessage',message)
        received = newclient.get_received()
        follow = received[1]
        self.assertEqual(follow['name'], 'follow_message')
        self.assertEqual(follow['args'][0]['message'], message['messagetosend'])
        self.assertEqual(follow['args'][0]['sender'], self.socketclient.sid)
        self.assertEqual(follow['namespace'], '/')
        newclient.disconnect()
        

if __name__ == '__main__':
    unittest.main()

