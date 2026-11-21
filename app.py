
from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, join_room
import secrets

app = Flask(__name__)
app.config["SECRET_KEY"] = "queueup-secret"

socketio = SocketIO(app, async_mode="threading")

# Store all queue rooms
rooms = {}


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# CREATE QUEUE
@app.route("/create", methods=["POST"])
def create_queue():

    room_code = secrets.token_hex(3).upper()

    rooms[room_code] = {
        "participants": [],
        "current": None
    }

    return redirect(url_for("host", room_code=room_code))


# HOST DASHBOARD
@app.route("/host/<room_code>")
def host(room_code):

    if room_code not in rooms:
        return "Queue not found!", 404

    return render_template(
        "host.html",
        room_code=room_code,
        participants=rooms[room_code]["participants"],
        current=rooms[room_code]["current"]
    )


# JOIN QUEUE
@app.route("/join", methods=["POST"])
def join_queue():

    participant_name = request.form.get(
        "participant_name", ""
    ).strip()

    room_code = request.form.get(
        "room_code", ""
    ).strip().upper()

    if not participant_name:
        return "Please enter your name!", 400

    if room_code not in rooms:
        return "Invalid room code!", 404

    rooms[room_code]["participants"].append(participant_name)

    position = len(rooms[room_code]["participants"])

    # Notify everyone about the updated queue
    socketio.emit(
        "queue_updated",
        {
            "participants": rooms[room_code]["participants"],
            "current": rooms[room_code]["current"]
        },
        to=room_code
    )

    return render_template(
        "participant.html",
        participant_name=participant_name,
        room_code=room_code,
        position=position,
        current=rooms[room_code]["current"]
    )


# CALL NEXT PARTICIPANT
@app.route("/call_next/<room_code>", methods=["POST"])
def call_next(room_code):

    if room_code not in rooms:
        return "Queue not found!", 404

    participants = rooms[room_code]["participants"]

    called = None

    if participants:

        # Remove only the first participant
        called = participants.pop(0)

        # Update currently serving participant
        rooms[room_code]["current"] = called

    else:
        rooms[room_code]["current"] = None

    # Notify host AND all participants
    socketio.emit(
        "queue_updated",
        {
            "participants": participants,
            "current": rooms[room_code]["current"],
            "called": called
        },
        to=room_code
    )

    return redirect(url_for("host", room_code=room_code))


# SOCKET.IO ROOM CONNECTION
@socketio.on("join_room")
def handle_join_room(data):

    if not isinstance(data, dict):
        return

    room_code = data.get("room_code", "").strip().upper()

    if room_code in rooms:

        join_room(room_code)

        # Send current queue information to the newly connected user
        socketio.emit(
            "queue_updated",
            {
                "participants": rooms[room_code]["participants"],
                "current": rooms[room_code]["current"]
            },
            to=request.sid
        )


# START SERVER
if __name__ == "__main__":
    socketio.run(app, debug=True)
