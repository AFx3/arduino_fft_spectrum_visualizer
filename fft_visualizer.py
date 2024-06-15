import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.signal import butter, lfilter

# read from the serial port at 115200 baud rate
ser = serial.Serial('/dev/ttyACM0', 115200) 

# plot initialization
fig, ax = plt.subplots()                            # creates a figure and a set of subplots  
bars = ax.bar(range(32), np.zeros(32))              # creates a bar chart with 32 bars initialized to zero height


# function to read FFT data from the serial port
def get_fft_data():
    try:
        # read a line from the serial port, decodes it from UTF-8, and strips any whitespace
        line = ser.readline().decode('utf-8').strip()
        # split the line into individual strings, converts them to floats, stores them in a list
        data = list(map(float, line.split()))
        if len(data) == 32:   
            return data
        else:
            return None
    except:
        return None

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs                                              # Nyquist frequency
    normal_cutoff = cutoff / nyq                                # normalize the cutoff frequency    
    # create a high-pass filter with a Butterworth design
    b, a = butter(order, normal_cutoff, btype='high', analog=False) 
    return b, a                                                 # return the numerator (b) and denominator (a) polynomials of the IIR filter

def highpass_filter(data, cutoff, fs, order=5):                 # apply the high-pass filter to the data
    b, a = butter_highpass(cutoff, fs, order=order)             # get the filter coefficients
    y = lfilter(b, a, data)                                     # apply the filter to the data
    return y                                                    # return the filtered data

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# function to update the heights of the bars (animation)
def update(frame):
    data = None
    # read data until a full frame is received
    while data is None:
        # get the FFT data
        data = get_fft_data()
    
    if filter_choice == 1:
        data = highpass_filter(data, cutoff_freq, sampling_rate)
    elif filter_choice == 2:
        data = lowpass_filter(data, cutoff_freq, sampling_rate)
    
    # update the heights of the bars in the plot
    for bar, height in zip(bars, data):
        bar.set_height(height)
    return bars                                                 # return the updated plot

# set plot parameters
ax.set_ylim(0, 10000) 
ax.set_xlabel('Frequency Bin')
ax.set_ylabel('Amplitude')
ax.set_title('Real-Time FFT of Microphone Input')

def main():
    global filter_choice, cutoff_freq, sampling_rate

    filter_choice = int(input("Enter 0 to see the sampled signal, 1 for high-pass filter, 2 for low-pass filter: "))
    
    if filter_choice in [1, 2]:
        cutoff_freq = float(input("Enter the cutoff frequency in Hz (must be less than 500 Hz): "))
        if cutoff_freq >= 500:
            raise ValueError("Cutoff frequency must be less than half of the sampling rate (500 Hz).")
        sampling_rate = 1000 
    
    # update the plot every 100 ms
    ani = FuncAnimation(fig, update, blit=True, interval=100, cache_frame_data=False)  

    plt.show()

if __name__ == "__main__":
    main()
