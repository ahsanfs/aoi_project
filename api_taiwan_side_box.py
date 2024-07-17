import rospy
from std_msgs.msg import String
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from datetime import datetime
import time as t
import math as mt
from utilsFS100 import FS100
from azure.iot.device import IoTHubDeviceClient, Message
from azure.iot.hub import IoTHubRegistryManager
import serial
import time

# API address
DEVICE_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;DeviceId=pchucenrotia;SharedAccessKey=Kk804zzExKPcQPlXiRNMSYe1dMbG0tpL8AIoTIA+4UU="
HUB_CONNECTION_STRING = "HostName=hucenrotiaiotfree.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=3qNeDGp0K5rZi+yTYW9IKFFGcOU1zwTSnAIoTIxa93Y="
DEVICE_ID = "laptop"

# Serial connection settings
serial_port = '/dev/ttyACM0'
baud_rate = 115200
stop_threads = False
ser = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2)

def calculate_velocity(distance, time):
    velocity = distance / time
    return velocity

def get_time_difference_ms(start_time, end_time):
    time_diff = end_time - start_time
    time_diff_ms = time_diff.total_seconds() * 1000
    return time_diff_ms

def calculate_movement_distance(position1, position2):
    distance = mt.sqrt(sum((position2[i] - position1[i])**2 for i in range(len(position1))))
    return distance

def remap(value, from_low, from_high, to_low, to_high):
    clamped_value = max(from_low, min(value, from_high))
    mapped_value = (clamped_value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low
    return mapped_value

def convert_mm(x, y, z, rx, ry, rz, re):
    str_x = "{:4d}.{:03d}".format(x // 1000, x % 1000)
    str_y = "{:4d}.{:03d}".format(y // 1000, y % 1000)
    str_z = "{:4d}.{:03d}".format(z // 1000, z % 1000)
    str_rx = "{:4d}.{:04d}".format(rx // 10000, rx % 10000)
    str_ry = "{:4d}.{:04d}".format(ry // 10000, ry % 10000)
    str_rz = "{:4d}.{:04d}".format(rz // 10000, rz % 10000)
    str_re = "{:4d}.{:04d}".format(re // 10000, re % 10000)

    x = float(str_x)
    y = float(str_y)
    z = float(str_z)
    rx = float(str_rx)
    ry = float(str_ry)
    rz = float(str_rz)
    re = float(str_re)

    input = [x, y, z, rx, ry, rz, re]
    return input

def rob_command(post1):
    x_coor = post1[0] * 1000
    y_coor = post1[1] * 1000
    z_coor = post1[2] * 1000
    rx_coor = post1[3] * 10000
    ry_coor = post1[4] * 10000
    rz_coor = post1[5] * 10000
    re_coor = post1[6] * 10000

    robot_command = [(int(x_coor), int(y_coor), int(z_coor), int(rx_coor), int(ry_coor), int(rz_coor), int(re_coor))]
    return robot_command

def update_pos():
    while stop_sign.acquire(blocking=False):
        stop_sign.release()
        t.sleep(0.02)

def is_alarmed():
    alarmed = True
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        alarmed = status['alarming']
    return alarmed

def on_reset_alarm():
    robot.reset_alarm(FS100.RESET_ALARM_TYPE_ALARM)
    t.sleep(0.1)
    is_alarmed()

class Job(threading.Thread):
    def __init__(self, post):
        super(Job, self).__init__()
        self.post = post

    def run(self):
        global speed
        if FS100.ERROR_SUCCESS == robot.read_position(pos_info, robot_no):
            x, y, z, rx, ry, rz, re = pos_info['pos']
            pointHome = [x, y, z, rx, ry, rz, re]

        PrevRobotPos = convert_mm(x, y, z, rx, ry, rz, re)

        if FS100.ERROR_SUCCESS == robot.get_status(status):
            if not status['servo_on']:
                robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)

        robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT, FS100.MOVE_SPEED_CLASS_MILLIMETER, speed, self.post, wait=True)

        if FS100.ERROR_SUCCESS == robot.read_position(pos_info, robot_no):
            x, y, z, rx, ry, rz, re = pos_info['pos']
            pointHome = [x, y, z, rx, ry, rz, re]
            straaa = "CURRENT POSITION\n" + \
                     "COORDINATE {:12s} TOOL:{:02d}\n".format('ROBOT', pos_info['tool_no']) + \
                     "R{} :X     {:4d}.{:03d} mm       Rx   {:4d}.{:04d} deg.\n".format(robot_no,
                                                                                        x // 1000, x % 1000,
                                                                                        rx // 10000,
                                                                                        rx % 10000) + \
                     "    Y     {:4d}.{:03d} mm       Ry   {:4d}.{:04d} deg.\n".format(
                         y // 1000, y % 1000, ry // 10000, ry % 10000) + \
                     "    Z     {:4d}.{:03d} mm       Rz   {:4d}.{:04d} deg.\n".format(
                         z // 1000, z % 1000, rz // 10000, rz % 10000) + \
                     "                            Re   {:4d}.{:04d} deg.\n".format(
                         re // 10000, re % 10000)
        print(straaa)

        robot.switch_power(FS100.POWER_TYPE_HOLD, FS100.POWER_SWITCH_ON)
        robot.switch_power(FS100.POWER_TYPE_HOLD, FS100.POWER_SWITCH_OFF)

def ros_callback(data):
    binary_string = data.data
    for i, bit in enumerate(binary_string):
        if bit == '1':
            if not button_toggled[i]:
                clicked(i, from_ros=True)
        elif bit == '0':
            if button_toggled[i]:
                clicked(i, from_ros=True)

def ros_callback(data, from_azure=False, from_arduino=False):
    binary_string = data.data
    for i, bit in enumerate(binary_string):
        if bit == '1':
            if not button_toggled[i]:
                clicked(i, from_ros=True, from_azure=from_azure, from_arduino=from_arduino)
        elif bit == '0':
            if button_toggled[i]:
                clicked(i, from_ros=True, from_azure=from_azure, from_arduino=from_arduino)

def clicked(index, from_ros=False, from_azure=False, from_arduino=False):
    root.counter[index] += 1
    if button_toggled[index]:
        if from_arduino:
            return
        buttons[index].config(bootstyle=SUCCESS)
        labels[index]["text"] = f"Available"
    else:
        buttons[index].config(bootstyle=DANGER)
        labels[index]["text"] = f"Finished"
        if from_ros and from_azure:
            job = Job(positions[index])
            job.start()
            print("Start Job ", positions[index], index)
    button_toggled[index] = not button_toggled[index]

    if from_arduino:
        # publish_button_states()
        send_to_azure()

def publish_button_states():
    binary_string = ''.join(['1' if state else '0' for state in button_toggled])
    pub.publish(String(data=binary_string))

def send_to_azure():
    binary_string = ''.join(['1' if state else '0' for state in button_toggled])
    try:
        registry_manager = IoTHubRegistryManager(HUB_CONNECTION_STRING)
        registry_manager.send_c2d_message(DEVICE_ID, binary_string)
        rospy.loginfo("Message sent to Azure IoT Hub")
    except Exception as ex:
        rospy.logerr(f"Failed to send message to Azure IoT Hub: {ex}")

def message_handler(message):
    rospy.loginfo("Message received from Azure IoT Hub: {}".format(message.data))
    decoded_message = message.data.decode('utf-8')
    pub.publish(String(data=decoded_message))
    ros_callback(String(data=decoded_message), from_azure=True)

def read_from_arduino():
    global stop_threads
    while not stop_threads:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            if data:
                parse_data(data)
                
def parse_data(data):
    try:
        current_status, saved_status = data.split(' ')
        rospy.loginfo(f"Current Status: {current_status}")
        rospy.loginfo(f"Saved Status: {saved_status}")
        binary_string = format(int(saved_status), '012b')
        ros_callback(String(data=saved_status), from_arduino=True)
    except ValueError:
        rospy.logwarn(f"Received unexpected data format: {data}")

if __name__ == '__main__':
    rospy.init_node('/sub/button_status', anonymous=True)
    pub = rospy.Publisher('/pub/button_status', String, queue_size=10)

    client = IoTHubDeviceClient.create_from_connection_string(DEVICE_CONNECTION_STRING)
    client.on_message_received = message_handler

    robot = FS100('172.16.0.1')
    speed = 400
    pos_info = {}
    robot_no = 1
    status = {}
    stop_sign = threading.Semaphore()

    # Robot positions
    p1 = [321.979, -61.950, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p2 = [321.979, 22.854, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p3 = [321.979, 97.654, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p4 = [321.979, 174.449, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p5 = [423.958, 174.449, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p6 = [423.958, 97.654, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p7 = [423.958, 22.854, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p8 = [423.958, -61.950, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p9 = [533.552, -61.950, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p10 = [533.552, 22.854, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p11 = [533.552, 97.654, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]
    p12 = [533.552, 174.449, -50.709, 174.5088, -0.2997, 3.8606, 0.0000]

    post_1 = rob_command(p1)
    post_2 = rob_command(p2)
    post_3 = rob_command(p3)
    post_4 = rob_command(p4)
    post_5 = rob_command(p8)
    post_6 = rob_command(p7)
    post_7 = rob_command(p6)
    post_8 = rob_command(p5)
    post_9 = rob_command(p9)
    post_10 = rob_command(p10)
    post_11 = rob_command(p11)
    post_12 = rob_command(p12)

    positions = [post_1, post_2, post_3, post_4, post_5, post_6, post_7, post_8, post_9, post_10, post_11, post_12]

    root = ttk.Window()
    root.title("Simple Counter Taiwan")
    root.geometry("600x350")

    root.counter = [0] * 12
    button_toggled = [False] * 12

    buttons = []
    labels = []

    button_order = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]
    ]

    for row in button_order:
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)
        for i in row:
            button = ttk.Button(frame, text=f"SSD {i+1}", bootstyle=SUCCESS, command=lambda i=i: clicked(i), width=13)
            button.grid(row=0, column=row.index(i), padx=5, pady=5)
            buttons.append(button)
            
            label = ttk.Label(frame, text="Available")
            label.grid(row=1, column=row.index(i), padx=5, pady=5)
            labels.append(label)

    threading.Thread(target=lambda: rospy.spin()).start()

    box_thread = threading.Thread(target=read_from_arduino)
    box_thread.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        stop_threads = True
        box_thread.join()