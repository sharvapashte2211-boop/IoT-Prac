import RPi.GPIO as GPIO
import time

# digit to segment mapping
SEGMENTS = (0x3f, 0x06, 0x5b, 0x4f,
            0x66, 0x6d, 0x7d, 0x07,
            0x7f, 0x6f)

BRIGHT_TYPICAL = 2

class TM1637:
    def __init__(self, brightness=BRIGHT_TYPICAL):
        self.clk = 23
        self.dio = 24
        self.brightness = brightness & 0x07
        self.doublepoint = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.dio, GPIO.OUT)

    def start(self):
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)
        GPIO.output(self.dio, 0)
        GPIO.output(self.clk, 0)

    def stop(self):
        GPIO.output(self.clk, 0)
        GPIO.output(self.dio, 0)
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self.clk, 0)
            GPIO.output(self.dio, (data >> i) & 1)
            GPIO.output(self.clk, 1)

        GPIO.output(self.clk, 0)
        GPIO.setup(self.dio, GPIO.IN)
        ack = GPIO.input(self.dio)
        GPIO.setup(self.dio, GPIO.OUT)
        GPIO.output(self.clk, 1)
        return ack

    def SetBrightness(self, brightness):
        self.brightness = brightness & 0x07

    def ShowDoublepoint(self, on):
        self.doublepoint = on

    def Show(self, data):
        seg_data = []
        for i in range(4):
            seg = SEGMENTS[data[i]]
            if i == 1 and self.doublepoint:  # colon between digit 2 & 3
                seg |= 0x80
            seg_data.append(seg)

        self.start()
        self.write_byte(0x40)
        self.stop()

        self.start()
        self.write_byte(0xC0)
        for d in seg_data:
            self.write_byte(d)
        self.stop()

        self.start()
        self.write_byte(0x88 + self.brightness)
        self.stop()

    def Clear(self):
        self.Show([0, 0, 0, 0])
