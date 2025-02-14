'''
This script allow to read FFT data from an Arduino over a serial connection, processes the data, and visualizes it using Matplotlib. 
It also allows applying high-pass or low-pass filters to the data before visualization
'''
import serial                                       # used for serial communication with the Arduino
import matplotlib.pyplot as plt                     # used for plotting
import numpy as np                                  # used for numerical operations
from matplotlib.animation import FuncAnimation      # used for real-time animation
from scipy.signal import butter, lfilter            # used for signal processing

# Initialize serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Adjust '/dev/ttyACM0' to match your Arduino's serial port
'''
port linux: /dev/ttyACM0
port windows: COM3
'''

# Parameters: MUST MATCH THE ARDUINO CODE
sampling_rate = 1000    # in Hz, same as the Arduino code
num_samples = 128       # 128 samples, same as the Arduino code
max_freq_nyquist = sampling_rate / 2 # MAX FREQUENC_NSQ
# evaluate freq interval
frequencies = np.fft.fftfreq(num_samples, d=1/sampling_rate)[:num_samples // 2] # array of frequencies for the FFT plot


# reads a line of data from the serial port, decodes it, and splits it into a list of floats
def get_fft_data():
    try:
        line = ser.readline().decode('utf-8').strip()
        data = list(map(float, line.split()))
        if len(data) == num_samples // 2:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error reading serial data: {e}")
        return None


# update function calls get_fft_data() to read data from the serial port until valid data is received
# applies a high-pass or low-pass filter based on the filter_choice
# updates the plot with the new data

def update(frame):
    data = None
    while data is None:
        data = get_fft_data()
    
    if filter_choice == 1:
        data = highpass_filter(data, cutoff_freq, sampling_rate)
        ax.set_title('FFT of Microphone Input - High-Pass Filter Applied')
    elif filter_choice == 2:
        data = lowpass_filter(data, cutoff_freq, sampling_rate)
        ax.set_title('FFT of Microphone Input - Low-Pass Filter Applied')
    else:
        ax.set_title('FFT of Microphone Input - Raw Signal')
    
    line.set_ydata(data) # updates the y-data of the plot
    # return the updated line for the animation.
    return line,


### plot initialization

fig, ax = plt.subplots()                                   # generate a new figure and axis for the plot
line, = ax.plot(frequencies, np.zeros(num_samples // 2))   # initializes a line plot with the frequencies array on the x-axis and an array of zeros on the y-axis 

# set the y-axis limits to 0-200 and the x-axis limits to 0-Nyquist frequency (500 Hz) and set the axis labels and the initial title of the plot
ax.set_ylim(0, 200)
ax.set_xlim(0, max_freq_nyquist)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')
ax.set_title('Real-Time FFT of Microphone Input')




def butter_highpass(cutoff, fs, order=5):
    max_nyq = 0.5 * fs                                              # Nyquist frequency
    normal_cutoff = cutoff / max_nyq                                # normalize the cutoff frequency    
    # create a high-pass filter with a Butterworth design
    b, a = butter(order, normal_cutoff, btype='high', analog=False) 
    return b, a                                                 # return the numerator (b) and denominator (a) polynomials of the IIR filter

def highpass_filter(data, cutoff, fs, order=5):                 # apply the high-pass filter to the data
    b, a = butter_highpass(cutoff, fs, order=order)             # get the filter coefficients
    y = lfilter(b, a, data)                                     # apply the filter to the data
    return y                                                    # return the filtered data

def butter_lowpass(cutoff, fs, order=5):
    max_nyq = 0.5 * fs 
    normal_cutoff = cutoff / max_nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def main():
    global filter_choice, cutoff_freq

    filter_choice = int(input("Enter 0 to see the sampled signal, 1 for high-pass filter, 2 for low-pass filter: "))
    
    if filter_choice in [1, 2]:
        cutoff_freq = float(input("Enter the cutoff frequency in Hz (must be less than 500 Hz): "))
        if cutoff_freq >= max_freq_nyquist:
            raise ValueError("Cutoff frequency must be less than half of the sampling rate (500 Hz).")
    
    ani = FuncAnimation(fig, update, blit=True, interval=100, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    main()
