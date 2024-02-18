import threading 
import zmq


class SystemStatusClient(threading.Thread):
    def __init__(self, app, ip_address):
        super().__init__()
        self.running = False

        self.app = app

        context = zmq.Context.instance()
        self.system_status_socket = context.socket(zmq.SUB)
        self.system_status_socket.connect(f"tcp://{ip_address}:5000")
        print("System status socket set up")
        self.system_status_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        
        self.values_dict = {
            "jetson_temperature": None,
            "jetson_power_usage": None,
            "memory_usage": None,
            "cpu_usage": None
        }

    def run(self):
        self.running = True
        while self.running:
            message = self.system_status_socket.recv_string()
            print(f"Received: {message}")

            for value_set in message.split(","):
                measure, value = value_set.split(":")
                self.values_dict[measure] = round(float(value),2)

            self.app.updateSystemMeasures(self.values_dict)
                

    def stop(self):
        self.running = False 
        self.system_status_socket.close()

