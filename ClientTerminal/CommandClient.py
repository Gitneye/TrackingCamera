import zmq

class Commander:
    def __init__(self, ip_address) -> None:
        socket_context = zmq.Context()
        self.socket = socket_context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{ip_address}:5050")

    def send_message(self, message):
        self.socket.send_string(message)
        response = self.socket.recv_string()
        print(f"Received response: {response}")

    def close_socket(self):
        self.socket.close()
