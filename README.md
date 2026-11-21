# QueueUp – Real-Time Queue Management System

A real-time queue management application built using Python, Flask, Flask-SocketIO, JavaScript, HTML and CSS.

## Features

- Create queue rooms with unique room codes.
- Allow multiple participants to join using a room code.
- Display waiting participants.
- Update queue positions automatically.
- Call participants sequentially.
- Display the currently serving participant.
- Notify participants when it is their turn.
- Real-time updates between host and participant dashboards without page refresh.

## Technologies Used

- Python
- Flask
- Flask-SocketIO
- JavaScript
- HTML
- CSS
- WebSockets

## How to Run

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
4. Open `http://127.0.0.1:5000` in your browser.

## Project Status

Core queue creation, participant joining, sequential queue advancement and real-time notifications are implemented.

Queue information is currently stored temporarily in application memory.
