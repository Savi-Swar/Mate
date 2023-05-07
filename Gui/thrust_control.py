import struct
import serial
import time

class SerialComms:
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
        self.values = [125, 125, 125, 125, 125, 150]
        self.neutral_offset = [0, 0, 15, 15, 15, 0]
        self.enable_neutral = False
        #              l    r    b    fl   fr   claw

    def get_real_values(self):
        return [self.values[i] + (self.neutral_offset[i] if self.enable_neutral else 0) for i in range(6)]

    def update(self):
        self.ser.write(bytes([0x7a, *[max(0, min(250, round(i))) for i in self.get_real_values()], 0xa7]))

    # default front axis (move forward)
    def forward(self, speed=1, offset=0):
        assert -1 <= speed <= 1
        self.values[0] += 125 * speed - offset * 125 * speed
        self.values[1] += 125 * speed + offset * 125 * speed

    # no strafe (z axis)

    # default up/down (y axis)
    def up(self, speed=1, r_offset=0, v_offset=0):
        self.values[2] += 125 * speed + v_offset * 125 * speed
        self.values[3] += 125 * speed - v_offset * 125 * speed - r_offset * 125 * speed
        self.values[4] += 125 * speed - v_offset * 125 * speed + r_offset * 125 * speed

    # default roll (roll cw)
    def roll(self, speed=1):
        self.values[3] += 125 * speed
        self.values[4] -= 125 * speed

    #default pitch (pitch up)
    def pitch(self, speed=1):
        self.values[2] += 125 * speed
        self.values[3] -= 62.5 * speed
        self.values[4] -= 62.5 * speed

    # default yaw (turn right)
    def yaw(self, speed=1):
        assert -1 <= speed <= 1
        self.values[1] += 125 * speed
        self.values[0] -= 125 * speed

    def claw(self, num):
        self.values[5] += num
        self.values[5] = min(250, max(60, self.values[5]))

    def reset(self):
        self.values = [125, 125, 125, 125, 125, 150]
        self.enable_neutral = False

    def toggle_neutral(self):
        self.enable_neutral = not self.enable_neutral

if __name__ == "__main__":
    sc = SerialComms(input("port: "))
    while True:
        m = input("> ")
        if m == "fw":
            sc.forward(float(input("speed> ")))
        if m == "up":
            sc.up(float(input("speed> ")))
        if m == "ro":
            sc.roll(float(input("speed> ")))
        if m == "pi":
            sc.pitch(float(input("speed> ")))
        if m == "ya":
            sc.yaw(float(input("speed> ")))
        if m == "claw":
            sc.claw(int(input("num> ")))
        if m == "values":
            print(sc.values)
        if m == "reset":
            sc.reset()
        if m == "exit":
            sc.reset()
            sc.update()
            sc.ser.close()
            exit()
        sc.update()
            