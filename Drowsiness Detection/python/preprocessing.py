"""
Implicit emotional state recognition technology based on physiological signal
(SW for user status (drowsiness, concentration,...) classification using heart rate information)

Code Description:
    Modules for preprocessing (band-pass filter) and segmentation averaging

This work was supported by Institute for information & communications
Technology Promotion(IITP) grant funded by the Korea government(MISP).
(No.2017-0-00167, Development of Human Implicit/Explicit Intention Recognition
Technologies for Autonomous Human-Things Interaction) and Basic
Science Research Program through the National Research Foundation of Korea
(NRF) funded by the Ministry of Education (2016R1D1A1B03934014).

Young-Seok Choi, Hyeon Kyu Lee, Dae-Young Lee
Department of Electronics and Communications Engineering
Kwangwoon University, Seoul, Korea
"""

import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    """Butterworth filter (low pass)

    Args:
        cutoff: cut off frequency
        fs: sampling frequency
        order: order of butterworth filter

    Returns:
        filter
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order):
    """Calculate filtered signal

    Args:
        data: signal
        cutoff: cut off frequency
        fs: sampling frequency
        order: order of butterworth filter

    Returns:
        low pass filtered signal
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def average(data, n):
    """Segmentation and averaging

    Args:
        data: data
        n: samples number of averaged data

    Returns:
        averaged signal
    """
    avg = []
    if (np.mod(np.shape(data)[1], n) == 0) or (round(np.shape(data)[1]/n) == int(np.shape(data)[1]/n)):
        s = int(np.shape(data)[1]/n)*2-1
    else:
        s = int(np.shape(data)[1]/n)*2
    
    for i in range(n):
        if i == 0:
            avg = np.transpose(np.mean(data[:, i*int(s/2+1) : i*int(s/2+1)+s-1], axis=1)[np.newaxis])
        else:
            if i*int(s/2+1)+s-1 > np.shape(data)[1]:
                if i*int(s/2+1) > np.shape(data)[1]:
                    break
                else:
                    if np.isnan(np.mean(data[:, i*int(s/2+1): np.shape(data)[1]], axis=1)[0]):
                        break
                    
                    tmp = np.transpose(np.mean(data[:, i*int(s/2+1): np.shape(data)[1]], axis=1)[np.newaxis])
                    avg = np.hstack((avg, tmp))
            else:
                if np.isnan(np.mean(data[:, i*int(s/2+1): np.shape(data)[1]], axis=1)[0]):
                    break
                tmp = np.transpose(np.mean(data[:, i*int(s/2+1): i*int(s/2+1)+s-1], axis=1)[np.newaxis])
                avg = np.hstack((avg, tmp))
            
    return avg

