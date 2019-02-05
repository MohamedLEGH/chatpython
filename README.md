# chatpython

[![Build Status](https://travis-ci.org/MohamedLEGH/chatpython.svg?branch=master)](https://travis-ci.org/MohamedLEGH/chatpython)

A simple web chat with python, flask and socketio

```
git clone https://github.com/MohamedLEGH/chatpython
```

# Build

(need docker)

```
cd chatpython

docker build -t chatpython .
```

# Run

```
cd chatpython

docker run -d -p 5000:5000 chatpython
```

# Test

```
cd chatpython

docker run chatapp python3 test_server.py

docker run chatapp coverage run test_server.py
```
