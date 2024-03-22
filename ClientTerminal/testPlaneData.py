import zmq
import json
import numpy as np
from PIL import Image
import threading
from datetime import datetime

class testClient(threading.Thread):
    def __init__(self,app,ip_address) -> None:
        threading.Thread.__init__(self)
        self.running = False

        self.app = app
        context = zmq.Context()

        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{ip_address}:5555")
        print("Plane data socket set up")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    def run(self):
        self.running = True
        while self.running:
        # Receive the message
            message = self.socket.recv_string()

            # Deserialize the JSON message
            data = json.loads(message)

        # Process the received data
            numpy_array_list = data["frame"]
            frame_size = data["frame_size"]
            numpy_array = np.array(numpy_array_list, dtype=np.float64)
            numpy_array = numpy_array.reshape((frame_size[1], frame_size[0]))  # Adjust the shape as needed
            print("Received NumPy array:")
            print(numpy_array)

            numpy_array_uint8 = numpy_array.astype(np.uint8)
            image = Image.fromarray(numpy_array_uint8)
            image.save('test_image.jpg')
            print("Image saved")

            list_data = data["stateList"]

            print("Received list data:")
            print(list_data)

            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S %d-%m-%Y")
            
            self.app.update_app(list_data, numpy_array, formatted_time, None)


    def stop(self):
        self.running = False
        self.socket.close()