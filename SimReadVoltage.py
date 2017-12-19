import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

adc_val = adc.read_adc(0, gain=GAIN)
print('Digital Value: ' + str(adc_val))
voltage = (3.3 * adc_val) / 26551
print('Voltage Value: ' + str(voltage))
voltage = str(round(voltage, 2))
print(voltage)
