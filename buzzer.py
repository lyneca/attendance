import time

#pylint: disable=import-error
import RPi.GPIO as GPIO

PIN = 15
FREQ_LOW = 400
FREQ_MED = 600
FREQ_HIGH = 800

SMALL_DELAY = 0.01
LONG_DELAY = 0.1


class Buzzer:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN, GPIO.OUT)
        self.buzzer = GPIO.PWM(15, FREQ_LOW)

    def buzz(self, freq):
        self.buzzer.ChangeFrequency(freq)
        self.buzzer.start(1)
        time.sleep(LONG_DELAY)
        self.buzzer.stop()
        time.sleep(SMALL_DELAY)

    def success(self):
        """Generic success buzz"""
        self.buzz(FREQ_LOW)
        self.buzz(FREQ_HIGH)

    def error(self):
        """Generic error buzz"""
        self.buzz(FREQ_HIGH)
        self.buzz(FREQ_LOW)

    def setup_error(self):
        """Called when the device errored in the setup stage"""
        self.buzz(FREQ_HIGH)
        self.buzz(FREQ_MED)
        self.buzz(FREQ_LOW)

    def setup_complete(self):
        """Called when the device is ready to process cards"""
        self.buzz(FREQ_LOW)
        self.buzz(FREQ_MED)
        self.buzz(FREQ_HIGH)

    def set_config(self):
        """Called when the device has had its config set"""
        self.buzz(FREQ_MED)
        self.buzz(FREQ_MED)
        self.buzz(FREQ_MED)

    def ready(self):
        """Called when the device initially boots"""
        self.buzz(FREQ_LOW)
        self.buzz(FREQ_LOW)


if __name__ == '__main__':
    buzzer = Buzzer()
    buzzer.success()
    time.sleep(1)
    buzzer.error()
    time.sleep(1)
    buzzer.setup_complete()
    time.sleep(1)
    buzzer.setup_error()
