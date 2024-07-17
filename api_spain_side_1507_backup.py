# # import rospy
# # from std_msgs.msg import String
# # import ttkbootstrap as ttk
# # from ttkbootstrap.constants import *
# # import threading
# # from azure.iot.device import IoTHubDeviceClient
# # from azure.iot.hub import IoTHubRegistryManager

# # # wait until the robot finish
# # # "111100000000, robot status (R), human inspecting (H)"

# # # Robot Inspection - Actions
# # # 0 = Unfinished = GRAY
# # # 1 = Robot Inspecting.. = BLUE  
# # # 2 = Accepted = GREEN
# # # 3 = Ask for help = YELLOW
# # # 4 = Rejected = RED

# # # Human Actions
# # # 0 = Unfinished = GRAY
# # # 5 = Human Inspecting.. = BLUE
# # # 6 = Accepted = GREEN
# # # 7 = Recheck = YELLOW
# # # 8 = Rejected = RED

# # # API address
# # DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
# # HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
# # DEVICE_ID = "pchucenrotia"

# # class ButtonControllerNode:
# #     def __init__(self, root, buttons, labels):
# #         rospy.init_node('aoi', anonymous=True)
# #         self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
# #         self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

# #         self.root = root
# #         self.buttons = buttons
# #         self.labels = labels
# #         self.button_toggled = [False] * len(buttons)

# #         self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
# #         self.device_client.on_message_received = self.message_handler
# #         self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

# #     def listener_callback(self, msg):
# #         binary_string = msg.data
# #         rospy.loginfo(f'Received: {binary_string}')
        
# #         for i, char in enumerate(binary_string):
# #             if char == '1':
# #                 if not self.button_toggled[i]:
# #                     self.toggle_button(i, from_subscriber=True)
# #             elif char == "2":
# #                 print("Waiting")
# #             elif char == '0':
# #                 if self.button_toggled[i]:
# #                     self.toggle_button(i, from_subscriber=True)

# #     def toggle_button(self, index, from_subscriber=False):
# #         if self.button_toggled[index]:
# #             self.buttons[index].config(bootstyle=DANGER)
# #             self.labels[index]["text"] = f"Available"
# #         else:
# #             self.buttons[index].config(bootstyle=SUCCESS)
# #             self.labels[index]["text"] = f"Finished"
# #         self.button_toggled[index] = not self.button_toggled[index]
        
# #         if from_subscriber:
# #             self.publish_button_states()
# #             self.send_to_azure()

# #     def publish_button_states(self):
# #         binary_string = ''.join(['1' if state else '0' for state in self.button_toggled])
# #         self.publisher.publish(String(data=binary_string))

# #     def send_to_azure(self):
# #         binary_string = ''.join(['1' if state else '0' for state in self.button_toggled])
# #         try:
# #             self.registry_manager.send_c2d_message(DEVICE_ID, binary_string)
# #             rospy.loginfo("Message sent to Azure IoT Hub")
# #         except Exception as ex:
# #             rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

# #     def message_handler(self, message):
# #         rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
# #         decoded_message = message.data.decode('utf-8')
# #         self.listener_callback(String(data=decoded_message))

# # def on_button_click(index, controller):
# #     controller.toggle_button(index)

# # def main():
# #     root = ttk.Window()
# #     root.title("Simple Counter Spain")
# #     root.geometry("600x350")

# #     buttons = []
# #     labels = []

# #     button_order = [
# #         [0, 1, 2, 3],
# #         [4, 5, 6, 7],
# #         [8, 9, 10, 11]
# #     ]

# #     for row in button_order:
# #         row_frame = ttk.Frame(root)
# #         row_frame.pack(padx=10, pady=10)
# #         for i in row:
# #             button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle=DANGER, width=13)
# #             button.grid(row=0, column=row.index(i), padx=5, pady=5)
# #             buttons.append(button)
            
# #             label = ttk.Label(row_frame, text="Available")
# #             label.grid(row=1, column=row.index(i), padx=5, pady=5)
# #             labels.append(label)

# #     button_controller_node = ButtonControllerNode(root, buttons, labels)
    
# #     for i, button in enumerate(buttons):
# #         button.config(command=lambda i=i: on_button_click(i, button_controller_node))
    
# #     threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

# #     root.mainloop()

# # if __name__ == '__main__':
# #     main()


# # import rospy
# # from std_msgs.msg import String
# # import ttkbootstrap as ttk
# # from ttkbootstrap.constants import *
# # import threading
# # from azure.iot.device import IoTHubDeviceClient
# # from azure.iot.hub import IoTHubRegistryManager

# # # Constants for Azure IoT Hub
# # DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
# # HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
# # DEVICE_ID = "pchucenrotia"

# # # Status mapping
# # STATUS_MAPPING = {
# #     '0': {'label': "Unfinished", 'color': SECONDARY},
# #     '1': {'label': "Robot Inspecting..", 'color': PRIMARY},
# #     '2': {'label': "Accepted (Robot)", 'color': SUCCESS}, #based on inspection accuracy >80%
# #     '3': {'label': "Ask for help", 'color': WARNING}, #based on inspection accuracy 60% - 80%
# #     '4': {'label': "Rejected (Robot)", 'color': DANGER}, #based on inspection accuracy <60%
# #     '5': {'label': "Human Inspecting..", 'color': PRIMARY},
# #     '6': {'label': "Accepted (Human)", 'color': SUCCESS}, #how to get or change status from these 3 states?
# #     '7': {'label': "Recheck", 'color': WARNING},
# #     '8': {'label': "Rejected (Human)", 'color': DANGER},
# #     '9': {'label': "Robot going to ..", 'color': DARK} #give red border on this
# # }

# # class ButtonControllerNode:
# #     def __init__(self, root, buttons, labels):
# #         rospy.init_node('aoi', anonymous=True)
# #         self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
# #         self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

# #         self.root = root
# #         self.buttons = buttons
# #         self.labels = labels
# #         self.button_status = ['0'] * len(buttons)  # Initialize all buttons to 'Unfinished' status

# #         self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
# #         self.device_client.on_message_received = self.message_handler
# #         self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

# #     def listener_callback(self, msg):
# #         status_string = msg.data
# #         rospy.loginfo(f'Received: {status_string}')
        
# #         for i, char in enumerate(status_string):
# #             self.update_button_status(i, char, from_subscriber=True)

# #     def update_button_status(self, index, status, from_subscriber=False):
# #         status_info = STATUS_MAPPING.get(status, {'label': "Unknown", 'color': SECONDARY})
# #         self.buttons[index].config(bootstyle=status_info['color'])
# #         self.labels[index]["text"] = status_info['label']
# #         self.button_status[index] = status
        
# #         if from_subscriber:
# #             self.publish_button_states()
# #             self.send_to_azure()

# #     def publish_button_states(self):
# #         status_string = ''.join(self.button_status)
# #         self.publisher.publish(String(data=status_string))

# #     def send_to_azure(self):
# #         status_string = ''.join(self.button_status)
# #         try:
# #             self.registry_manager.send_c2d_message(DEVICE_ID, status_string)
# #             rospy.loginfo("Message sent to Azure IoT Hub")
# #         except Exception as ex:
# #             rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

# #     def message_handler(self, message):
# #         rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
# #         decoded_message = message.data.decode('utf-8')
# #         self.listener_callback(String(data=decoded_message))

# # def on_button_click(index, controller):
# #     # For this example, we'll cycle through statuses for the button when clicked
# #     current_status = controller.button_status[index]
# #     next_status = str((int(current_status) + 1) % 9)  # Cycle through statuses 0-8
# #     controller.update_button_status(index, next_status)


# # def toggle_fullscreen(self, event=None):
# #     self.state = not self.state  # Just toggling the boolean
# #     self.tk.attributes("-fullscreen", self.state)
# #     return "break"

# # def end_fullscreen(self, event=None):
# #     self.state = False
# #     self.tk.attributes("-fullscreen", False)
# #     return "break"
    
# # def main():
# #     root = ttk.Window()
# #     root.attributes("-fullscreen", True)
# #     root.title("Simple Counter Spain")
# #     # root.bind("<F11>", self.toggle_fullscreen)
# #     # root.bind("<Escape>", self.end_fullscreen)
# #     # root.geometry("600x350")

# #     buttons = []
# #     labels = []

# #     button_order = [
# #         [0, 1, 2, 3],
# #         [4, 5, 6, 7],
# #         [8, 9, 10, 11]
# #     ]

# #     for row in button_order:
# #         row_frame = ttk.Frame(root)
# #         row_frame.pack(padx=10, pady=10)
# #         for i in row:
# #             button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle=SECONDARY, width=13)
# #             button.grid(row=0, column=row.index(i), padx=5, pady=5)
# #             buttons.append(button)
            
# #             label = ttk.Label(row_frame, text="Unfinished")
# #             label.grid(row=1, column=row.index(i), padx=5, pady=5)
# #             labels.append(label)

# #     button_controller_node = ButtonControllerNode(root, buttons, labels)
    
# #     for i, button in enumerate(buttons):
# #         button.config(command=lambda i=i: on_button_click(i, button_controller_node))
    
# #     threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

# #     root.mainloop()

# # if __name__ == '__main__':
# #     main()

# import rospy
# from std_msgs.msg import String
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import threading
# from azure.iot.device import IoTHubDeviceClient
# from azure.iot.hub import IoTHubRegistryManager

# # Constants for Azure IoT Hub
# DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
# HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
# DEVICE_ID = "pchucenrotia"

# # Status mapping
# STATUS_MAPPING = {
#     '0': {'label': "Unfinished", 'color': 'CustomSecondary_2.TButton'},
#     '1': {'label': "Robot Inspecting..", 'color': 'CustomPrimary.TButton'},
#     '2': {'label': "Accepted (Robot)", 'color': 'CustomSuccess.TButton'}, #based on inspection accuracy >80%
#     '3': {'label': "Ask for help", 'color': WARNING}, #based on inspection accuracy 60% - 80%
#     '4': {'label': "Rejected (Robot)", 'color': DANGER}, #based on inspection accuracy <60%
#     '5': {'label': "Human Inspecting..", 'color': PRIMARY},
#     '6': {'label': "Accepted (Human)", 'color': SUCCESS}, #how to get or change status from these 3 states?
#     '7': {'label': "Recheck", 'color': WARNING},
#     '8': {'label': "Rejected (Human)", 'color': DANGER},
#     '9': {'label': "Robot going to ..", 'color': DARK}
# }

# # give like a status label, to show the meaning

# class ButtonControllerNode:
#     def __init__(self, root, buttons, labels):
#         rospy.init_node('aoi', anonymous=True)
#         self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
#         self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

#         self.root = root
#         self.buttons = buttons
#         self.labels = labels
#         self.button_status = ['0'] * len(buttons)  # Initialize all buttons to 'Unfinished' status

#         self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
#         self.device_client.on_message_received = self.message_handler
#         self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

#         # Create custom styles for border colors
#         style = ttk.Style()
#         style.configure('CustomSecondary_2.TButton', font=('Helvetica', 20), borderwidth=0, padding=0, background='#CFCFC4', foreground='#FFFFFF')
#         style.configure('CustomRed.TButton', font=('Helvetica', 20), padding=0, background='#FFFFFF', bordercolor='red', lightcolor='#FF0000', darkcolor='#0000FF', borderwidth=5, foreground='#000000')
#         style.configure('CustomBlue.TButton', font=('Helvetica', 20), relief="solid", bordercolor='red', borderwidth=5)
#         style.configure('CustomPrimary.TButton', font=('Helvetica', 20), padding=0, relief="solid")
#         style.configure('CustomSuccess.TButton', font=('Helvetica', 20), padding=0, bootstyle='#77DD77', relief="solid")
#         style.configure('CustomWarning.TButton', font=('Helvetica', 20), padding=0, background='#FDFD96', relief="solid")
#         style.configure('CustomDanger.TButton', font=('Helvetica', 20), padding=0, background='#FF6961', relief="solid")
#         style.configure('Asw.TButton', font=('Helvetica', 20))
#         style.configure('Large.TButton', background='#808080', foreground='#FFFFFF', font=("Helvetica", 20))
#         style.configure('CustomSecondary.TButton', background='secondary', foreground='white', font=('Helvetica', 20))

#     def listener_callback(self, msg):
#         status_string = msg.data
#         rospy.loginfo(f'Received: {status_string}')
        
#         for i, char in enumerate(status_string):
#             self.update_button_status(i, char, from_subscriber=True)

#     def update_button_status(self, index, status, from_subscriber=False):
#         status_info = STATUS_MAPPING.get(status, {'label': "Unknown", 'color': 'Asw.TButton'})
#         if status == '9':
#             self.buttons[index].config(style='CustomRed.TButton')
#         elif status == '1':
#             self.buttons[index].config(style='CustomBlue.TButton')
#         elif status == '2':
#             self.buttons[index].config(style='CustomSuccess.TButton')
#         elif status == '3':
#             self.buttons[index].config(style='CustomWarning.TButton')
#         elif status == '4':
#             self.buttons[index].config(style='CustomDanger.TButton')
#         elif status == '5':
#             self.buttons[index].config(style='CustomPrimary.TButton')
#         elif status == '6':
#             self.buttons[index].config(style='CustomSuccess.TButton')
#         elif status == '7':
#             self.buttons[index].config(style='CustomWarning.TButton')
#         elif status == '8':
#             self.buttons[index].config(style='CustomDanger.TButton')
#         elif status == '0':
#             self.buttons[index].config(style='Asw.TButton')
#         else:
#             self.buttons[index].config(bootstyle=status_info['color'])
#         self.labels[index]["text"] = status_info['label']
#         self.button_status[index] = status
        
#         if from_subscriber:
#             self.publish_button_states()
#             self.send_to_azure()

#     def publish_button_states(self):
#         status_string = ''.join(self.button_status)
#         self.publisher.publish(String(data=status_string))

#     def send_to_azure(self):
#         status_string = ''.join(self.button_status)
#         try:
#             self.registry_manager.send_c2d_message(DEVICE_ID, status_string)
#             rospy.loginfo("Message sent to Azure IoT Hub")
#         except Exception as ex:
#             rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

#     def message_handler(self, message):
#         rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
#         decoded_message = message.data.decode('utf-8')
#         self.listener_callback(String(data=decoded_message))

# def on_button_click(index, controller):
#     current_status = controller.button_status[index]
#     next_status = str((int(current_status) + 1) % 10)
#     controller.update_button_status(index, next_status)

# def toggle_fullscreen(event=None):
#     root.attributes("-fullscreen", not root.attributes("-fullscreen"))
#     return "break"

# def main():
#     global root
#     root = ttk.Window()
#     root.title("Simple Counter Spain")
#     root.geometry("800x600")

#     buttons = []
#     labels = []
    
#     style = ttk.Style()
#     # style.configure('CustomSecondary_2.TButton', font=('Helvetica', 20), borderwidth=0, background='#CFCFC4', foreground='#FFFFFF')
#     style.configure('Asw.TButton', font=('Helvetica', 20))

#     button_order = [
#         [0, 1, 2, 3],
#         [4, 5, 6, 7],
#         [8, 9, 10, 11]
#     ]

#     for row in button_order:
#         row_frame = ttk.Frame(root)
#         row_frame.pack(padx=10, pady=10, expand=True)
#         for i in row:
#             button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle='success', style='Asw.TButton', width=10, padding=10)
#             button.grid(row=0, column=row.index(i), padx=10, pady=10, ipady=20, ipadx=20)
#             buttons.append(button)
            
#             label = ttk.Label(row_frame, text="Unfinished", font=("Helvetica", 20))
#             label.grid(row=1, column=row.index(i), padx=10, pady=10)
#             labels.append(label)

#     button_controller_node = ButtonControllerNode(root, buttons, labels)
    
#     for i, button in enumerate(buttons):
#         button.config(command=lambda i=i: on_button_click(i, button_controller_node))

#     root.bind("<F11>", toggle_fullscreen)
    
#     threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

#     root.mainloop()

# if __name__ == '__main__':
#     main()

# import rospy
# from std_msgs.msg import String
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# import threading
# from azure.iot.device import IoTHubDeviceClient
# from azure.iot.hub import IoTHubRegistryManager

# # Constants for Azure IoT Hub
# DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
# HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
# DEVICE_ID = "pchucenrotia"

# # Status mapping
# STATUS_MAPPING = {
#     '0': {'label': "Unfinished", 'color': SECONDARY},
#     '1': {'label': "Robot Inspecting..", 'color': PRIMARY},
#     '2': {'label': "Accepted (Robot)", 'color': SUCCESS}, #based on inspection accuracy >80%
#     '3': {'label': "Ask for help", 'color': WARNING}, #based on inspection accuracy 60% - 80%
#     '4': {'label': "Rejected (Robot)", 'color': DANGER}, #based on inspection accuracy <60%
#     '5': {'label': "Human Inspecting..", 'color': PRIMARY},
#     '6': {'label': "Accepted (Human)", 'color': SUCCESS}, #how to get or change status from these 3 states?
#     '7': {'label': "Recheck", 'color': WARNING},
#     '8': {'label': "Rejected (Human)", 'color': DANGER},
#     '9': {'label': "Robot going to ..", 'color': DARK}
# }

# class ButtonControllerNode:
#     def __init__(self, root, buttons, labels):
#         rospy.init_node('aoi', anonymous=True)
#         self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
#         self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

#         self.root = root
#         self.buttons = buttons
#         self.labels = labels
#         self.button_status = ['0'] * len(buttons)  # Initialize all buttons to 'Unfinished' status

#         self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
#         self.device_client.on_message_received = self.message_handler
#         self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

#         # Create custom styles for border colors
#         style = ttk.Style()
#         style.configure('CustomRed.TButton', font=('Helvetica', 20), background='#FFFFFF', bordercolor='red', lightcolor='#FF0000', darkcolor='#0000FF', borderwidth=5, foreground='#000000')
#         style.configure('CustomBlue.TButton', font=('Helvetica', 20), relief="solid", bordercolor='red', borderwidth=5)
#         style.configure('Large.TButton', background='#808080', foreground='#FFFFFF', font=("Helvetica", 20))
#         style.configure('custom.TButton', background='red', foreground='white', font=('Helvetica', 24))

#     def listener_callback(self, msg):
#         status_string = msg.data
#         rospy.loginfo(f'Received: {status_string}')
        
#         for i, char in enumerate(status_string):
#             self.update_button_status(i, char, from_subscriber=True)

#     def update_button_status(self, index, status, from_subscriber=False):
#         status_info = STATUS_MAPPING.get(status, {'label': "Unknown", 'color': 'custom.TButton'})
#         if status == '9':
#             self.buttons[index].config(style='CustomRed.TButton')
#         elif status == '1':
#             self.buttons[index].config(style='CustomBlue.TButton')
#         else:
#             self.buttons[index].config(bootstyle=status_info['color'])
#         self.labels[index]["text"] = status_info['label']
#         self.button_status[index] = status
        
#         if from_subscriber:
#             self.publish_button_states()
#             self.send_to_azure()

#     def publish_button_states(self):
#         status_string = ''.join(self.button_status)
#         self.publisher.publish(String(data=status_string))

#     def send_to_azure(self):
#         status_string = ''.join(self.button_status)
#         try:
#             self.registry_manager.send_c2d_message(DEVICE_ID, status_string)
#             rospy.loginfo("Message sent to Azure IoT Hub")
#         except Exception as ex:
#             rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

#     def message_handler(self, message):
#         rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
#         decoded_message = message.data.decode('utf-8')
#         self.listener_callback(String(data=decoded_message))

# def on_button_click(index, controller):
#     current_status = controller.button_status[index]
#     next_status = str((int(current_status) + 1) % 10)
#     controller.update_button_status(index, next_status)

# def toggle_fullscreen(event=None):
#     root.attributes("-fullscreen", not root.attributes("-fullscreen"))
#     return "break"

# def main():
#     global root
#     root = ttk.Window(themename="superhero")
#     root.title("Simple Counter Spain")
#     root.geometry("800x600")

#     buttons = []
#     labels = []

#     button_order = [
#         [0, 1, 2, 3],
#         [4, 5, 6, 7],
#         [8, 9, 10, 11]
#     ]

#     for row in button_order:
#         row_frame = ttk.Frame(root)
#         row_frame.pack(padx=10, pady=10, expand=True)
#         for i in row:
#             button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle=SECONDARY, width=40)
#             button.grid(row=0, column=row.index(i), padx=10, pady=10, ipady=20, ipadx=20)
#             buttons.append(button)
            
#             label = ttk.Label(row_frame, text="Unfinished", font=("Helvetica", 20))
#             label.grid(row=1, column=row.index(i), padx=10, pady=10)
#             labels.append(label)

#     button_controller_node = ButtonControllerNode(root, buttons, labels)
    
#     for i, button in enumerate(buttons):
#         button.config(command=lambda i=i: on_button_click(i, button_controller_node))

#     root.bind("<F11>", toggle_fullscreen)
    
#     threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

#     root.mainloop()

# if __name__ == '__main__':
#     main()


import rospy
from std_msgs.msg import String
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from azure.iot.device import IoTHubDeviceClient
from azure.iot.hub import IoTHubRegistryManager

# Constants for Azure IoT Hub
DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=laptop;SharedAccessKey=opy0hBVpRH6h465Kz2nHs0rLhS9N2wyniAIoTD66DlY="
HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
DEVICE_ID = "pchucenrotia"

# Status mapping
STATUS_MAPPING = {
    '0': {'label': "Unfinished", 'color': SECONDARY},
    '1': {'label': "Robot Inspecting..", 'color': PRIMARY},
    '2': {'label': "Accepted (Robot)", 'color': SUCCESS}, #based on inspection accuracy >80%
    '3': {'label': "Ask for help", 'color': WARNING}, #based on inspection accuracy 60% - 80%
    '4': {'label': "Rejected (Robot)", 'color': DANGER}, #based on inspection accuracy <60%
    '5': {'label': "Human Inspecting..", 'color': PRIMARY},
    '6': {'label': "Accepted (Human)", 'color': SUCCESS}, #how to get or change status from these 3 states?
    '7': {'label': "Recheck", 'color': WARNING},
    '8': {'label': "Rejected (Human)", 'color': DANGER},
    '9': {'label': "Robot going to ..", 'color': DARK}
}

class ButtonControllerNode:
    def __init__(self, root, buttons, labels):
        rospy.init_node('aoi', anonymous=True)
        self.publisher = rospy.Publisher('/pub/aoi/spain/status', String, queue_size=10)
        self.subscriber = rospy.Subscriber('/sub/aoi/spain/status', String, self.listener_callback)

        self.root = root
        self.buttons = buttons
        self.labels = labels
        self.button_status = ['0'] * len(buttons)  # Initialize all buttons to 'Unfinished' status

        self.device_client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
        self.device_client.on_message_received = self.message_handler
        self.registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)

        # Create custom styles for border colors and fonts
        style = ttk.Style()
        style.configure('CustomRed.TButton', background='#FFFFFF', bordercolor='red', lightcolor='#FF0000', darkcolor='#0000FF', borderwidth=5, foreground='#000000')
        style.configure('CustomBlue.TButton', relief="solid", bordercolor='red', borderwidth=5)
        style.configure('Large.TButton', background='#808080', foreground='#FFFFFF', font=("Helvetica", 20))
        style.configure('custom.TButton', background='red', foreground='white', font=('Helvetica', 20))
        style.configure('TButton', font=('Helvetica', 20))

    def listener_callback(self, msg):
        status_string = msg.data
        rospy.loginfo(f'Received: {status_string}')
        
        for i, char in enumerate(status_string):
            self.update_button_status(i, char, from_subscriber=True)

    def update_button_status(self, index, status, from_subscriber=False):
        status_info = STATUS_MAPPING.get(status, {'label': "Unknown", 'color': 'custom.TButton'})
        if status == '9':
            self.buttons[index].config(style='CustomRed.TButton')
        elif status == '1':
            self.buttons[index].config(style='CustomBlue.TButton')
        else:
            self.buttons[index].config(bootstyle=status_info['color'])
        self.labels[index]["text"] = status_info['label']
        self.button_status[index] = status
        
        if from_subscriber:
            self.publish_button_states()
            self.send_to_azure()

    # def update_button_status(self, index, status, from_subscriber=False):
    #     status_info = STATUS_MAPPING.get(status, {'label': "Unknown", 'color': 'custom.TButton'})
    #     self.buttons[index].config(bootstyle=status_info['color'])
    #     self.labels[index]["text"] = status_info['label']
    #     self.button_status[index] = status
        
    #     if from_subscriber:
    #         self.publish_button_states()
    #         self.send_to_azure()

    def publish_button_states(self):
        status_string = ''.join(self.button_status)
        self.publisher.publish(String(data=status_string))

    def send_to_azure(self):
        status_string = ''.join(self.button_status)
        try:
            self.registry_manager.send_c2d_message(DEVICE_ID, status_string)
            rospy.loginfo("Message sent to Azure IoT Hub")
        except Exception as ex:
            rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

    def message_handler(self, message):
        rospy.loginfo(f"Message received from Azure IoT Hub: {message.data}")
        decoded_message = message.data.decode('utf-8')
        self.listener_callback(String(data=decoded_message))

def on_button_click(index, controller):
    current_status = controller.button_status[index]
    next_status = str((int(current_status) + 1) % 10)
    controller.update_button_status(index, next_status)

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    return "break"

def main():
    global root
    root = ttk.Window()
    root.title("Simple Counter Spain")
    root.geometry("800x600")

    buttons = []
    labels = []

    button_order = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]
    ]

    for row in button_order:
        row_frame = ttk.Frame(root)
        row_frame.pack(padx=10, pady=10, expand=True)
        for i in row:
            button = ttk.Button(row_frame, text=f"SSD {i+1}", bootstyle=SECONDARY, width=20)
            button.grid(row=0, column=row.index(i), padx=10, pady=10, ipady=40, ipadx=20)
            buttons.append(button)
            
            label = ttk.Label(row_frame, text="Unfinished", font=("Helvetica", 20))
            label.grid(row=1, column=row.index(i), padx=10, pady=10)
            labels.append(label)

    button_controller_node = ButtonControllerNode(root, buttons, labels)
    
    for i, button in enumerate(buttons):
        button.config(command=lambda i=i: on_button_click(i, button_controller_node))

    root.bind("<F11>", toggle_fullscreen)
    
    threading.Thread(target=lambda: rospy.spin(), daemon=True).start()

    root.mainloop()

if __name__ == '__main__':
    main()
