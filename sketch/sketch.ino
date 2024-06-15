#include <arduinoFFT.h>

// consts
#define SAMPLES 64               // # samples, must be  even       
#define SAMPLING_FREQUENCY 1000   // sampling max feq 1 Khz, so sampled signal max 500 Hz


ArduinoFFT<double> FFT = ArduinoFFT<double>();

unsigned int sampling_period_us;  // will be evaluated according to SAMPLING_FREQUENCY (ms)
unsigned long microseconds;       // save current time in ms

// Vreal contains samples at the end the spectrum
// VImag for imaginary part
double vReal[SAMPLES];
double vImag[SAMPLES];

void setup() {
  Serial.begin(115200);
  sampling_period_us = round(1000000 * (1.0 / SAMPLING_FREQUENCY)); // *1000000 to get ms
}

void loop() {
  // sampling
  for (int i = 0; i < SAMPLES; i++) {
    
    // save time in current ms to set up sempling to get regular
    microseconds = micros();    
    
    vReal[i] = analogRead(A0); // read samples form A0 pin
    vImag[i] = 0;

    while (micros() < (microseconds + sampling_period_us)) {
      // freeze until interval sampled time is elapsed
    }
  }

  
  FFT.windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD); 
  FFT.compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.complexToMagnitude(vReal, vImag, SAMPLES);

  // print results
  for (int i = 0; i < (SAMPLES / 2); i++) {
    // print the frequency amplitude 
    Serial.print(vReal[i]);
    Serial.print(" ");
  }
  Serial.println();
  delay(100);
}