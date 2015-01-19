from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

socketio = SocketIO(app)

@app.route('/')
def index():
    print 'hello'
    #return render_template('index.html')
    emit('my response', {'data': message['data']})

@socketio.on('my event', namespace='/test')
def test_message(message):
    print 'test_message'
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

if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",port=7778)