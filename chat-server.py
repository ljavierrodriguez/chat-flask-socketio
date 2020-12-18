from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'abc123'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/chat")
def chat():
    return render_template('index.html')

@socketio.on('connected')
def connected(data):
    print(data)


@socketio.on("message")
def get_message(json, methods=['POST']):
    print("mensaje:" + str(json))
    room = json["room"]
    socketio.emit("response", json, room=room)


@socketio.on('join')
def join_room(data):
    print("join to: ", data)
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    socketio.emit("response join", username + " se ha unido a la sala(" + room + ")")

@socketio.on('leave')
def left_room(data):
    print("disconnect", data)
    username = data["username"]
    room = data["room"]
    leave_room(room)
    socketio.emit("response leave", username + " ha dejado la sala(" + room + ")" )

if __name__ == "__main__":
    socketio.run(app)