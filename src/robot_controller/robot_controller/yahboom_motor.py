import serial
import time

# Serial setup
ser = serial.Serial(
    port='/dev/ttyUSB0',  
    baudrate=115200,
    timeout=1
)

# Wheel mapping
WHEEL_MAP = {
    "front_left": 0,
    "rear_left": 1,
    "front_right": 2,
    "rear_right": 3,
}

# Low-level serial send
def control_speed(m1, m2, m3, m4):
    cmd = f"$spd:{m1},{m2},{m3},{m4}#"
    ser.write(cmd.encode())
    time.sleep(0.02)

"""""
def set_motor_deadzone(deadzone_value, motor=None):def set_motor_deadzone(deadzone_value, motor=None):def set_motor_deadzone(deadzone_value, motor=None):
set_motor_deadzone(1600, motor=1)  # front_left
set_motor_deadzone(1650, motor=2)  # front_right
set_motor_deadzone(1600, motor=3)  # rear_left (the slow-starting one)
set_motor_deadzone(1600, motor=4)  # rear_right
"""


# Wheel speed abstraction
def send_wheel_speeds(speeds):
    motor_cmd = [0, 0, 0, 0]
    for wheel, speed in speeds.items():
        motor_cmd[WHEEL_MAP[wheel]] = speed
    control_speed(*motor_cmd)

# High-level motion functions
def drive_forward(speed):
    send_wheel_speeds({
        "front_left":  speed,
        "rear_left":   -speed - 50,
        "front_right": speed,
        "rear_right":  -speed,
    })

def drive_backward(speed):
    send_wheel_speeds({
        "front_left":  -speed,
        "rear_left":   speed + 50,
        "front_right": -speed,
        "rear_right":  speed,
    })

def stop_robot():
    send_wheel_speeds({
        "front_left": 0,
        "rear_left": 0,
        "front_right": 0,
        "rear_right": 0,
    })

if __name__== "__main__":
    drive_forward(300)
    time.sleep(2)
    stop_robot()
    print("SERIAL OPENED")
