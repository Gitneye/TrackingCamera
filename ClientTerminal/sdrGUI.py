import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from time import sleep
import signal
import sys

from testPlaneData import testClient
from SystemStatusClient import SystemStatusClient
from CommandClient import Commander

class GUIApp:
        
    def __init__(self):
        self.image_path = "revolution_aero.jpeg"
        self.data = ["N/A", "N/A","N/A"]
        self.time = "N/A"

        self.root = tk.Tk()
        self.root.title("ADSB GUI")
        self.style = ttk.Style()


    def startScreen(self):

        screen_width = self.root.winfo_screenwidth()
        font_size = int(screen_width / 90)
        font_type = "Helvetica"
        #Left Half
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Create and display time label on top left
        self.time_label = tk.Label(self.left_frame,text=f'Datetime: {self.time}', font=(font_type, int(font_size*0.7)))
        self.time_label.grid(row=0,column=0,padx=10,pady=10)

        # Create and display an image on the left side
        self.image_label = tk.Label(self.left_frame)
        self.image_label.grid(row=1,column=0,padx=10,pady=10)

        #Create and display buttons on bottom left

        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.grid(row=2,column=0,padx=5,pady=5)

        self.filesButton = tk.Button(self.button_frame, text="Files", font=(font_type, font_size))
        self.filesButton.grid(row=0, column=0, padx=20, pady=5)

        self.fanButton = tk.Button(self.button_frame, text="Pause", font=(font_type, font_size), command=self.pause)
        self.fanButton.grid(row=0, column=1, padx=20, pady=5)

        self.stopButton = tk.Button(self.button_frame, text="Stop", font=(font_type, font_size), command=shutdown)
        self.stopButton.grid(row = 0, column = 2, padx=20, pady=5)
        
        # Right Half
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Create and display storage label on top right
        self.storage_label = tk.Label(self.right_frame, text="Storage: N/A", font=(font_type, int(font_size*0.7)))
        self.storage_label.grid(row=0,column=0,padx=10,pady=10)

        self.style.configure("Treeview", font=(font_type, int(font_size*0.5)))
        self.style.configure("Treeview.Heading", font=(font_type, int(font_size*0.65), "bold"))

        # Create a table (treeview) on the right side
        self.tree = ttk.Treeview(self.right_frame, columns=("ICAO", "Category", "Position"), show="headings")
        self.tree.heading("ICAO", text="ICAO")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Position",text="Position")
        self.tree.grid(row=0, column=1, padx=10, pady=10)
        self.tree.grid(row=1,column=0,padx=10,pady=10)
        self.tree.column("Position", width=300, anchor="center")
        self.tree.column("ICAO", anchor="center")
        self.tree.column("Category", anchor="center")

        self.jetson_temperature_label = tk.Label(self.right_frame, text= "Jetson Temperature: ---- Celsius", font=(font_type, int(font_size*0.8)))
        self.jetson_temperature_label.grid(row=2,column=0,padx=10,pady=5)

        self.jetson_power_label = tk.Label(self.right_frame, text= "Jetson Power Usage: ---- W", font=(font_type, int(font_size*0.8)))
        self.jetson_power_label.grid(row=3,column=0,padx=10,pady=5)

        self.memory_label = tk.Label(self.right_frame, text="Memory Usage: ----", font=(font_type, int(font_size*0.8)))
        self.memory_label.grid(row=4,column=0,padx=10,pady=5)

        self.cpu_label = tk.Label(self.right_frame, text="CPU Usage: ----", font=(font_type, int(font_size*0.8)))
        self.cpu_label.grid(row=5,column=0,padx=10,pady=5)

        # Add sample data to the table
        self.populate_table(self.data)
        # Load and display an image
        self.load_image(self.image_path)
        

    def populate_table(self,data):
        # Insert sample data into the table
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert("", "end", values=(data[0], data[1], data[2]))

    def update_table(self,stateList):
        for item in self.tree.get_children():
                self.tree.delete(item)
        for i in range(len(stateList)):
            stateVector = stateList[i]
            self.tree.insert("", i, values=(stateVector[0], stateVector[2], "(Latitude: " + str(stateVector[3])
                                            +"; \nLongitude: "+str(stateVector[4])+"; \nAltitude: "+str(stateVector[5])+")"))

    def load_image(self, image_path):
        # Load and display an image on the left side
        try:
            image = Image.open(image_path)
            image = image.resize((640,480))
            img = ImageTk.PhotoImage(image)
            self.image_label.config(image=img)
            self.image_label.image = img
        except Exception as e:
            print(f"Error loading image: {e}")

    def update_image(self,frame):

        image = Image.fromarray(frame)
        image = image.resize((640,480))
        img = ImageTk.PhotoImage(image)
        self.image_label.config(image=img)
        self.image_label.image = img
        
    def update_app(self,stateList,frame,time,storage):
        self.update_table(stateList)
        self.update_image(frame)
        self.time = time
        self.time_label.config(text=f'Datetime: {self.time}')
        self.storage_label.config(text=f'Storage: {storage}')

    def updateSystemMeasures(self, values_dict):
        self.jetson_temperature_label.config(text=f'Jetson Temperature:{values_dict["jetson_temperature"]} Celsius')
        self.jetson_power_label.config(text=f'Jetson Power Usage: {values_dict["jetson_power"]} W')
        self.cpu_label.config(text=f'CPU Usage: {values_dict["cpu_usage"]}')
        self.memory_label.config(text=f'Memory Usage: {values_dict["memory_usage"]}')

    def pause(self):
        if self.fanButton.cget("text") == "Pause":
            self.fanButton.config(text="Resume")
            commander.send_message("Pause")

        elif self.fanButton.cget("text") == "Resume":
            self.fanButton.config(text="Pause") 
            commander.send_message("Resume")
            


def signal_handler(sig,frame):
    print("Ctrl+C pressed. Exiting...")
    data.stop()
    data.join()
    app.root.destroy()

def shutdown():
    print("Shutting down...")
    commander.send_message("Shutdown")
    data.stop()
    data.join()
    status_client.stop()
    status_client.join()
    app.root.destroy()
    

if __name__ == "__main__":
    
    app = GUIApp()
    commander = Commander(ip_address=sys.argv[1])
    data = testClient(app=app, ip_address=sys.argv[1])
    status_client = SystemStatusClient(app=app, ip_address=sys.argv[1])

    signal.signal(signal.SIGINT,signal_handler)

    app.startScreen()

    sleep(5)
    
    data.start()
    status_client.start()

    app.root.mainloop()