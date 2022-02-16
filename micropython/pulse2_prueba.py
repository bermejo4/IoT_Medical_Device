from machine import Pin, Signal, I2C, ADC, Timer
import time

adc = ADC(0)



MAX_HISTORY = 250
TOTAL_BEATS = 30

def calculate_bpm(beats):
    # Truncate beats queue to max, then calculate bpm.
    # Calculate difference in time from the head to the
    # tail of the list. Divide the number of beats by
    # this duration (in seconds)
    beats = beats[-TOTAL_BEATS:]
    beat_time = beats[-1] - beats[0]
    if beat_time:
        bpm = (len(beats) / (beat_time)) * 60
        print("%d bpm" % bpm, 12, 0)

def detect():
    # Maintain a log of previous values to
    # determine min, max and threshold.
    history = []
    beats = []
    beat = False

    while True:
        conversion_factor = 1024 / (65535)
        v = adc.read_u16()*conversion_factor
        #print(v)
        

        history.append(v)

        # Get the tail, up to MAX_HISTORY length
        history = history[-MAX_HISTORY:]

        minima, maxima = min(history), max(history)

        threshold_on = (minima + maxima * 3) // 4   # 3/4
        threshold_off = (minima + maxima) // 2      # 1/2

        if v > threshold_on and beat == False:
            beat = True
            beats.append(time.time())
            beats = beats[-TOTAL_BEATS:]
            calculate_bpm(beats)

        if v < threshold_off and beat == True:
            beat = False
detect()