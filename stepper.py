from gpiozero import OutputDevice
from time import sleep

# กำหนด GPIO พินใหม่ (แก้ไขตามที่ติดตั้ง)
A1 = OutputDevice(4)   # GPIO 4
A2 = OutputDevice(17)  # GPIO 17
A3 = OutputDevice(27)  # GPIO 27
A4 = OutputDevice(22)  # GPIO 22

# ลำดับการหมุนของ Stepper Motor (Full Step Mode)
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

def set_pins(state):
    """ตั้งสถานะ GPIO ตามค่าในลำดับ step_sequence"""
    A1.value = state[0]
    A2.value = state[1]
    A3.value = state[2]
    A4.value = state[3]

def step_motor(direction, steps):
    """
    ควบคุมการหมุนของ Stepper Motor
    :param direction: ทิศทางการหมุน (1 = เดินหน้า, -1 = ถอยหลัง)
    :param steps: จำนวนก้าวที่ต้องการหมุน
    """
    delay = 0.001  # ล็อคค่าหน่วงเวลาไว้ที่ 0.001 วินาที
    forward_sequence = step_sequence
    backward_sequence = list(reversed(step_sequence))  # แปลง reversed เป็นลิสต์
    sequence = forward_sequence if direction > 0 else backward_sequence

    for _ in range(steps):
        for step in sequence:
            set_pins(step)
            sleep(delay)

try:
    while True:
        direction = int(input("กรุณาใส่ทิศทาง (1 = เดินหน้า, -1 = ถอยหลัง): "))
        steps = int(input("กรุณาใส่จำนวนก้าวที่ต้องการหมุน: "))
        
        if direction in [1, -1]:
            print(f"หมุน {steps} ก้าวในทิศทาง {'เดินหน้า' if direction == 1 else 'ถอยหลัง'}...")
            step_motor(direction, steps)
        else:
            print("กรุณากรอกทิศทางเป็น 1 หรือ -1 เท่านั้น")

except KeyboardInterrupt:
    print("ออกจากโปรแกรม...")

finally:
    # ปิดทุก GPIO เพื่อความปลอดภัย
    A1.off()
    A2.off()
    A3.off()
    A4.off()
