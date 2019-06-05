"""
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

The signal features are extracted through the CCA and
classified using the trained SVM model.

Since we load the SVM model stored through "pickle", 
we need to set the file name of the SVM model.

This is a two-class classification code.
"""
import bandfilt
import pickle
import numpy as np
from sklearn.cross_decomposition import CCA

class class_feature():
    
    def __init__(self):
        self.lowcut = 0.53
        self.highcut = 40
        self.fs = 256
        self.stimuli_time = 3
        self.t = np.linspace(0, self.stimuli_time, self.stimuli_time*self.fs)
        self.cca_frequency = [5.45, 12.0]                       
        self.channel = 32
        
    def CanonCoff(self, X):
        
        Y = [i for i in range(len(self.cca_frequency))]
        for i in range(len(self.cca_frequency)):
            ref = 2*np.pi*self.t*self.cca_frequency[i]
            Y[i] = [np.sin(ref),np.cos(ref),np.sin(2*ref), np.cos(2*ref)]
            
        print(len(X))
        cca=CCA(n_components = 4)        
        result= np.zeros((len(self.cca_frequency),4))
        
        for i in range(len(self.cca_frequency)):
            Z=np.array([Y[i]])
            X_c, Y_c = cca.fit_transform(X,Z[0].T)
            cca_value = np.corrcoef(X_c.T, Y_c.T)
            for k in range(4):
                result[i][k] = cca_value[0+k,4+k]
            result[i] = np.max(result[i])
        return result[:,0]
    

    def nispsvm(self,test):
        print('test len =',len(test))
        output = self.CanonCoff(bandfilt.butter_bandpass_filter(test,self.lowcut, self.highcut, self.fs))
        
        # Load SVM model
        with open('2class_factor.txt', 'rb') as f:
            svm = pickle.load(f) 
        y_pred_svc = svm.predict([output])
        return y_pred_svc