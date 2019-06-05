'''
This work was supported by Institute for information & communications
Technology Promotion(IITP) grant funded by the Korea government(MISP).
(No.2017-0-00167, Development of Human Implicit/Explicit Intention Recognition
Technologies for Autonomous Human-Things Interaction) and Basic
Science Research Program through the National Research Foundation of Korea
(NRF) funded by the Ministry of Education (2016R1D1A1B03934014).

Young-Seok Choi, Hyeon Kyu Lee, Ji-Hack Lee
Department of Electronics and Communications Engineering
Kwangwoon University, Seoul, Korea

===============================================================================

multi channel band pass filter
parameter of butterworth filter
 data : multi channel data
 lowcut : low cutoff frequency
 highcut : high cutoff frequency
 fs : sampling rate
 order : order of filter , default = 5
'''

from scipy.signal import butter, lfilter
import numpy as np

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):    
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    
    pos = data.shape
    filt_data = np.zeros((pos[0],pos[1]))
    
    for i in range(pos[1]):
        filt_data[:,i] = lfilter(b, a, data[:, i])
        
    return filt_data

