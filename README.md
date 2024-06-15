# Instructions for Running the Real-Time FFT Visualization Application

This guide will walk you through the steps required to set up a virtual environment using `venv` and run the real-time FFT visualization application.

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.x
- `pip3` (Python package installer)
- `virtualenv` package (optional, but recommended for managing virtual environments)

## Steps
### 0. Load the sketch to your Arduino UNO locatend inside 'sketch' folder 

```bash
cd sketch
```

### 1. Set Up a Virtual Environment

Create a virtual environment using `venv`:

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

- **On Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- **On macOS and Linux**:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Required Packages

With the virtual environment activated, install the necessary packages using `pip`:

```bash
pip3 install -r requirements.txt
```

### 4. Connect Your Arduino

Ensure your Arduino is connected to the correct serial port. You may need to modify the serial port setting in the script (e.g., `/dev/ttyACM0` for Linux, `COM3` for Windows).

### 5. Run the Application

Execute the Python script to start the real-time FFT visualization:

```bash
python fft_visualizer.py
```


### 7. Deactivate the Virtual Environment

Once you are done, deactivate the virtual environment:

```bash
deactivate
```

## Notes

- Make sure your Arduino is properly programmed to send FFT data to the serial port.
- Adjust the serial port name in the script to match your system's configuration.
- The application will prompt you to choose a filter type and, if applicable, a cutoff frequency.

By following these steps, you should be able to set up and run the real-time FFT visualization application in a clean and isolated Python environment.