import machine
import time

PWM_CONVERSION_HALF = 32768

if __name__=='__main__':

    # initialize pwm pin
    pwmLED = machine.PWM(machine.Pin(0))
    pwmLED.freq(1000)

    pwmLED.duty_u16(32768)
    time.sleep(2)

    while True:
        for i in range(10):
            value = (float(i) / 10) * PWM_CONVERSION_HALF
            pwmLED.duty_u16(int(value))
            time.sleep_ms(100)
        time.sleep(1)
        pwmLED.duty_u16(32768)
        for i in range(10):
            value = (float(i) / 10) * PWM_CONVERSION_HALF
            pwmLED.duty_u16(32768 - int(value))
            time.sleep_ms(100)
        pwmLED.duty_u16(0)
        time.sleep(1)