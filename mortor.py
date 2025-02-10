from gpiozero import PWMOutputDevice, DigitalOutputDevice

class MotorControl:
    def __init__(self):
        # Motor 1 (Back Left) pins
        self.motor_back_left_pwm = PWMOutputDevice(12)  # PWM pin for speed
        self.motor_back_left_dir = DigitalOutputDevice(13)  # Direction pin

        # Motor 2 (Back Right) pins
        self.motor_back_right_pwm = PWMOutputDevice(20)  # PWM pin for speed
        self.motor_back_right_dir = DigitalOutputDevice(21)  # Direction pin

    def validate_speed(self, speed):
        # Constrain speed to the range 0-1
        return max(0, min(speed, 1))

    def move_forward(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Stop motors before changing direction
        
        # Set both motors to move forward
        self.motor_back_left_dir.on()  # Direction forward
        self.motor_back_right_dir.on()  # Direction forward
        
        self.motor_back_right_pwm.on()
        self.motor_back_left_pwm.on()
        
        # self.motor_back_left_pwm.value = speed
        # self.motor_back_right_pwm.value = speed

    def move_backward(self, speed):
        speed = self.validate_speed(speed)
        self.stop()  # Stop motors before changing direction
        
        # Set both motors to move backward
        self.motor_back_left_dir.on()  # Direction backward
        self.motor_back_right_dir.off()  # Direction backward
        self.motor_back_left_pwm.off() 
        self.motor_back_right_pwm.on() 
        

    def turn_left(self, speed):
        speed = self.validate_speed(speed)
        self.stop()
        
        self.motor_back_left_dir.on()  # Left motor backward
        self.motor_back_right_dir.on()  # Right motor forward
        self.motor_back_left_pwm.off()
        self.motor_back_right_pwm.on() 
        
        # Turn left: slow/stop one motor, run the other
     
    def turn_right(self, speed):
        speed = self.validate_speed(speed)
        self.stop()
        
        # Turn right: slow/stop one motor, run the other
        self.motor_back_left_dir.on()  # Left motor forward
        self.motor_back_right_dir.on()  # Right motor backward
        self.motor_back_left_pwm.on()
        self.motor_back_right_pwm.off() 

        
        

    def stop(self):
        self.motor_back_left_pwm.off()  # หยุดส่งสัญญาณ PWM
        self.motor_back_right_pwm.off()  # หยุดส่งสัญญาณ PWM
        self.motor_back_left_dir.off()  # ปิด Direction
        self.motor_back_right_dir.off() 
