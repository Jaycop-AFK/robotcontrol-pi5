import asyncio
import websockets
import time
# from gpiozero import Servo 
from time import sleep
from gpiozero import OutputDevice
from mortor import MotorControl


A1 = OutputDevice(4)  # GPIO 4
A2 = OutputDevice(27)  # GPIO 17
A3 = OutputDevice(17)  # GPIO 27
A4 = OutputDevice(22)


step_sequence = [
    [1, 0, 0, 1],  # Step 1
    [1, 0, 0, 0],  # Step 2
    [1, 1, 0, 0],  # Step 3
    [0, 1, 0, 0],  # Step 4
    [0, 1, 1, 0],  # Step 5
    [0, 0, 1, 0],  # Step 6
    [0, 0, 1, 1],  # Step 7
    [0, 0, 0, 1],  # Step 8
]

# servo_pin = 23

# servo = Servo(servo_pin, min_pulse_width=0.0005, max_pulse_width=0.0025)

motor_control = MotorControl()


# def set_angle(angle):
#     """Set the servo to a specific angle and detach after a short delay."""
#     if angle < 0:
#         angle = 0
#     elif angle > 180:
#         angle = 180
    
#     # print(f"Setting servo angle to {angle}")
#     servo.value = round((angle - 90) / 90, 2)  # Normalize angle to servo range (-1 to 1)
#     time.sleep(0.5)  # Allow the servo to reach the target position
#     servo.detach() 

# angle = 45
# set_angle(angle)

# class MotorControl:
#     def move_forward(self, speed):
#         print(f"Motor moving forward at speed {speed}")
#         motors.move_forward(speed)
        
#     def move_backward(self, speed):
#         print(f"Motor moving backward at speed {speed}")
#         motors.move_backward(speed)

#     def turn_left(self, speed):
#         print(f"Motor turning left at speed {speed}")
#         motors.turn_left(speed)

#     def turn_right(self, speed):
#         print(f"Motor turning right at speed {speed}")
#         motors.turn_right(speed)

#     def stop(self):
#         print("Motor stopped")
#         motors.stop()

# motor_control = MotorControl()
current_speed = 100
angle = 45
angle_step = 2

def set_pins(state):
    """Set GPIO pins according to the current step state"""
    A1.value = state[0]
    A2.value = state[1]
    A3.value = state[2]
    A4.value = state[3]
    
    
def step_motor(direction, steps):
    """
    Control the stepper motor to rotate a specific number of steps
    :param direction: 1 for forward, -1 for backward
    :param steps: Number of steps to rotate
    """
    delay = 0.001  # Fixed delay between steps
    forward_sequence = step_sequence
    backward_sequence = list(reversed(step_sequence))  # Reverse sequence for backward motion
    sequence = forward_sequence if direction > 0 else backward_sequence

    for _ in range(steps):
        for step in sequence:
            set_pins(step)
            sleep(delay)

def rotate_motor_by_angle(degrees, direction):
    """
    Rotate the motor by a specific number of degrees
    :param degrees: Number of degrees to rotate
    :param direction: 1 for forward, -1 for backward
    """
    steps_per_revolution = 2048  # Number of steps per full rotation (360 degrees)
    steps_per_degree = steps_per_revolution / 360  # Steps per degree
    steps = int(degrees * steps_per_degree)  # Calculate total steps based on angle
    step_motor(direction, steps)


async def handle_client(websocket):
    global current_speed, angle
    
    # print(f"Client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            # print(f"Received from client: {message}")

            if isinstance(message, bytes): 
                payload = message
                if len(payload) == 1:
                    command = payload[0]
                    if command == 0x04: 
                        current_speed = min(current_speed + 100, 255)
                        print(f"Speed increased to {current_speed}")
                    elif command == 0x05: 
                        current_speed = max(current_speed - 100, 0)
                        print(f"Speed decreased to {current_speed}")
                        # print(f"Speed decreased to {current_speed}")
                        
                    elif command == 0x06: 
                        # print("up")
                        # angle += 18
                        # if angle > 90:
                        #     angle = 90
                        # set_angle(angle)
                        rotate_motor_by_angle(angle_step, -1)
                    elif command == 0x07: 
                        # print("down")
                        # angle -= 18
                        # if angle < 0:
                        #     angle = 0
                        # set_angle(angle)
                        rotate_motor_by_angle(angle_step, 1)
                    elif command == 0x08:
                        motor_control.turn_right(current_speed)
                    elif command == 0x09:
                        motor_control.turn_left(current_speed)
                    else:
                        motor_control.stop()
                elif len(payload) == 4:
                    direction = payload[0]
                    joystick_x = payload[2]
                    joystick_y = payload[3]
                    
                    if direction == 0x01: 
                        if joystick_y > 135: 
                            motor_control.move_forward(current_speed)
                        elif joystick_y < 120:
                            motor_control.move_backward(current_speed)
                        else:
                            motor_control.stop()
                            
                    elif direction == 0x02:
                
                        if joystick_y > 135: 
                            # print(current_speed)
                            motor_control.move_backward(current_speed)
                        elif joystick_y < 120:
                            # print(current_speed)
                            motor_control.move_forward(current_speed)
                        else:
                            motor_control.stop()
                    
                else:
                    motor_control.stop() 
            else:
                response = f"Server received your message: {message}"
                await websocket.send(response)

    except websockets.ConnectionClosed:
        # print(f"Connection with client {websocket.remote_address} closed")
        motor_control.stop()

    except Exception as e:
        # print(f"Error: {e}")
        motor_control.stop()

async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8003)
    # print("WebSocket server started at ws://0.0.0.0:8003")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())