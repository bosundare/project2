import os
from datetime import datetime

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

channels = {}

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        if 'user' not in session:
            return render_template("index.html")
        else:
            if 'channel' not in session:
                name = session["user"]
                return render_template("room.html", name = name, channels = channels)
            else:
                return render_template("chatroom.html", name = session["user"], channel = session["channel"], channels = channels)
    else:
        name = request.form.get('name')
        channel = request.form.get('channel')
        if name is not None:
            session['user'] = name
            return render_template("room.html", name = name, channels = channels)
        if channel is not None:
            session['channel'] = channel
            channels[channel] = []
            return render_template("chatroom.html", name = session['user'], channel = session['channel'], channels = channels)
        return render_template("index.html", message = "Enter valid information")

@app.route("/chatroom/<channel>", methods = ["POST", "GET"])
def chatroom(channel):
    session['channel'] = channel
    session['name'] = name
    return render_template("chatroom.html", name = session['user'], channel = channel, channels = channels)


@app.route("/logout")
def logout():
   # remove the username from the session if it is there
    session.pop('user', None)
    return render_template("index.html", message="You have successfully logged out")

@socketio.on("submit message")
def vote(data):
    time = datetime.now().strftime("%I:%M%p")
    channel = data["channel"]
    message = time + " [" + data['user'] +"]: " + data["message"]
    user = data['user']

    if len(channels[channel]) < 100:
        channels[channel].append(message)
    else:
        channels[channel].pop(0)
        channels[channel].append(message)
    emit("announce message", {'channel': channel, 'user': user, 'message': message}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
    print("Running through socketio.run")
