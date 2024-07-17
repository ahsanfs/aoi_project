import rospy
from std_msgs.msg import String
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from azure.iot.device import IoTHubDeviceClient
from azure.iot.hub import IoTHubRegistryManager

# wait until the robot finish

# API address
DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
DEVICE_ID = "pchucenrotia"

class ButtonControllerNode:
    def __init__(self, root, buttons, labels):
        rospy.init_node('aoi', anonymous=True)
        self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
        self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

        self.root = root
        self.buttons = buttons
        self.labels = labels
        self.button_toggled = [False] * len(buttons)

        self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
        self.device_client.on_message_received = self.message_handler
        self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

    def listener_callback(self, msg):
        binary_string = msg.data
        rospy.loginfo(f'Received: {binary_string}')
        
        for i, char in enumerate(binary_string):
            if char == '1':
                if not self.button_toggled[i]:
                    self.toggle_button(i, from_subscriber=True)
            elif char == '0':
                if self.button_toggled[i]:
                    self.toggle_button(i, from_subscriber=True)

    def toggle_button(self, index, from_subscriber=False):
        if self.button_toggled[index]:
            self.buttons[index].config(bootstyle=SUCCESS)
            self.labels[index]["text"] = f"Available"
        else:
            self.buttons[index].config(bootstyle=DANGER)
            self.labels[index]["text"] = f"Finished"
        self.button_toggled[index] = not self.button_toggled[index]
        
        if from_subscriber:
            self.publish_button_states()
            self.send_to_azure()

    def publish_button_states(self):
        binary_string = ''.join(['1' if state else '0' for state in self.button_toggled])
        self.publisher.publish(String(data=binary_string))

    def send_to_azure(self):
        binary_string = ''.join(['1' if state else '0' for state in self.button_toggled])
        try:
            self.registry_manager.send_c2d_message(DEVICE_ID, binary_string)
            rospy.loginfo("Message sent to Azure IoT Hub")
        except Exception as ex:
            rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

    def message_handler(self, message):
        rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
        decoded_message = message.data.decode('utf-8')
        self.listener_callback(String(data=decoded_message))

def on_button_click(index, controller):
    controller.toggle_button(index)

def main():
    root = ttk.Window()
    root.title("Simple Counter Spain")
    root.geometry("600x350")

    buttons = []
    labels = []

    button_order = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]
    ]

    for row in button_order:
        row_frame = ttk.Frame(root)
        row_frame.pack(padx=10, pady=10)
        for i in row:
            button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle=SUCCESS, width=13)
            button.grid(row=0, column=row.index(i), padx=5, pady=5)
            buttons.append(button)
            
            label = ttk.Label(row_frame, text="Available")
            label.grid(row=1, column=row.index(i), padx=5, pady=5)
            labels.append(label)

    button_controller_node = ButtonControllerNode(root, buttons, labels)
    
    for i, button in enumerate(buttons):
        button.config(command=lambda i=i: on_button_click(i, button_controller_node))
    
    threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

    root.mainloop()

if __name__ == '__main__':
    main()
