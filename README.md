# Intelligence-IoT

## Runtime Environment

### Windows 10 64bit
### SSVEP
* ### 27-inch LCD monitor, 60Hz
* ### Biosemi ActiveTwo
### Drowsiness detection
* ### Empatica E4


## Development Environment

### Biosemi Labview installation
* #### https://www.biosemi.com/download.htm
* #### Version : 8.06
### SSVEP
* #### Python3 installation
  * #### https://www.python.org/downloads/
* #### Spyder3 installation
       pip install spyder
* #### PsychoPy3.0.0 installation
   * #### https://github.com/psychopy/psychopy/releases

### Drowsiness detection
* #### Python3 installation
   * #### https://www.python.org/downloads/
* #### JAVA – Android Studio installation
   * #### https://developer.android.com/studio/?hl=ko

## Get Started

* ### SSVEP
   * #### Open the Biosemi Labview and setting the option(sampling rate, channel, etc.)
   * #### Setting the parameter of python
   * #### Start the Boisemi Labview
   * #### Execute python
* ### Drowsiness detection
   * #### Wrist wear and power on the Empatica E4 device
   * #### Connection with a PPG measurement program
   * #### Button control of the PPG measurement program
   * #### Offline: For storing PPG data
   * #### Online: Real-time PPG measurement and drowsiness recognition

## Overall description of source code

* ### SSVEP
   * #### Creating the visual stimulus of SSVEP
   * #### Acquisition of EEG data of SSVEP
   * #### Preprocessing the EEG data of SSVEP acquired.
   * #### Feature Extraction (Common Spatial Pattern, Canonical Correlation Analysis, etc.)
   * #### Classification (Linear Discriminant Analysis, Support Vector Machine)
* ### Drowsiness detection
   * #### Acquisition of user’s PPG data using PPG measuring device (‘Empatica E4’)
   * #### Real-time communication of acquired PPG data
   * #### Classifier model training using acquired PPG data (offline)
   * #### User state classification using PPG data acquired in real time (online)
