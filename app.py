from flask import Flask, request, render_template
import socket

app = Flask(__name__)

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the server address and port
server_address = ('0.0.0.0', 3001)  # Change the IP and port as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        udp_socket.sendto(message.encode(), server_address)
    return render_template('index.html')

@app.route('/receive')
def receive_message():
    try:
        data, addr = udp_socket.recvfrom(1024)
        message = data.decode()
    except socket.timeout:
        message = "No messages received yet."
    return render_template('index.html', received_message=message)

if __name__ == '__main__':
    udp_socket.bind(server_address)
    udp_socket.settimeout(1)  # Set a timeout for receiving messages
    app.run(host='0.0.0.0', debug=True)
