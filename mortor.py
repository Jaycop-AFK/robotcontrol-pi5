from gpiozero import PWMOutputDevice
import time
class MotorControl:
    def __init__(self):
        # Initialize motor pins as PWM devices
        self.motor_back_left_forward = PWMOutputDevice(12)
        self.motor_back_left_backward = PWMOutputDevice(13)
        
        self.motor_back_right_forward = PWMOutputDevice(20)
        self.motor_back_right_backward = PWMOutputDevice(21)

    def validate_speed(self, speed):
        # Constrain speed to the range 0-1 (since GPIOZero uses 0-1 for PWM)
        return max(0, min(speed, 1))


    def move_forward(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Ensure backward pins are off
        self.motor_back_left_backward.value = speed
        self.motor_back_right_forward.value = speed

    def move_backward(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Ensure forward pins are off
        self.motor_back_left_forward.value = speed
        self.motor_back_right_backward.value = speed

    def turn_left(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Ensure other pins are off
        
        
        self.motor_back_left_forward.value = speed
        self.motor_back_right_forward.value = speed

    def turn_right(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Ensure other pins are off
       
        
        self.motor_back_left_backward.value = speed
        self.motor_back_right_backward.value = speed

    def stop(self):
        # Stop all motors
        self.motor_back_left_forward.value = 0
        self.motor_back_left_backward.value = 0
        self.motor_back_right_forward.value = 0
        self.motor_back_right_backward.value = 0