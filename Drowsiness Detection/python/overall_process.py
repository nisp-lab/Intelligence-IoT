"""
Implicit emotional state recognition technology based on physiological signal
(SW for user status (drowsiness, concentration,...) classification using heart rate information)

Code Description:
    - Classifier model (SVM) training using acquired PPG data
    - Feature extraction (heart rate, RR interval, entropy)
    - Binary classification (awakening and drowsiness)

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
import peakutils
from sklearn.svm import SVC
from sklearn.model_selection import KFold
import csv
import preprocessing
from pyentrp.entropy import permutation_entropy as PE


class process_class:
    def __init__(self, sub_num):
        """Load PPG data

        Args:
           sub_num: number of subject
        """
        self.sub_num = sub_num
        self.ppg_D_set = {'subject' + str(sub_num): []}
        self.ppg_N_set = {'subject' + str(sub_num): []}

        f = open('./data/normal/subject' + str(sub_num) + '.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            self.ppg_N_set['subject' + str(sub_num)].append(line)
        f.close()

        f = open('./data/drowsiness/subject' + str(sub_num) + '.csv', 'r', encoding='utf-8')
        rdr = csv.reader(f)
        for line in rdr:
            self.ppg_D_set['subject' + str(sub_num)].append(line)
        f.close()

    ####################################################################################################################
    def feature_ext(self, signal, flag):
        """Feature extraction of PPG data

        Args:
           signal: PPG data
           flag: Identification for classifier training or real time prediction

        Returns:
            HR_set: Heart rate
            RR_set: RR interval
            mpe_set: Multiscale permutation entropy
        """
        ################################################################################################################
        # set parameters
        Fs = 64             # sampling frequency
        m = 4               # embedding dimension for PE
        t = 1               # time delay for PE
        num_entropy = 30    # the number of samples for PE
        w = Fs * 15         # window length
        HR_set = []         # list for heart rate feature
        RR_set = []         # list for RR interval feature
        pe_set = []  # list for heart rate feature

        if flag == 0:       # for classifier training
            sig = np.array(signal).astype(np.float)
            [R, L] = sig.shape
            num_window = round(L/w)

        else:               # for real time prediction
            sig = np.array(signal, dtype=np.float)[np.newaxis]
            [R, L] = sig.shape
            num_window = round(L/w)

        ################################################################################################################
        # feature extraction
        for i in range(0, R):
            for j in range(0, num_window):
                tmp_sig = sig[i, w * j:w * (j + 1)]
                # preprocessing (low pass filter)
                filtered = preprocessing.butter_lowpass_filter(tmp_sig, 2.5, 64.0, 5)
                # find peak point
                locs = peakutils.indexes(filtered, thres=0.4, min_dist=Fs * 0.5)

                for k in range(0, len(locs) - 1):
                    # calculate RR interval and heart rate
                    RR_set.append((locs[k + 1] - locs[k])/Fs)
                    HR_set.append(Fs / (locs[k + 1] - locs[k]) * 60)

        # Removing abnormal data: HR < 50, RR < 2 seconds
        HR_set = [i for i in HR_set if i>=50 and i<=120]
        RR_set = [i for i in RR_set if i<=2 and i>=0.5]

        # Calculate permutation entropy for RR interval (RR_set)
        # 50% overlapping
        q = 0
        while 1:
            if num_entropy+q*int(num_entropy/2) >= len(RR_set):
                tmp = RR_set[q*int(num_entropy/2):]
                pe_set.append(PE(tmp, m, t))
                break
            else:
                tmp = RR_set[q*int(num_entropy/2):num_entropy+q*int(num_entropy/2)]
                pe_set.append(PE(tmp, m, t))
                q += 1

        HR_set = np.array(HR_set, dtype=np.float)[np.newaxis]
        RR_set = np.array(RR_set, dtype=np.float)[np.newaxis]
        pe_set = np.array(pe_set, dtype=np.float)[np.newaxis]
        return HR_set, RR_set, pe_set

    ####################################################################################################################

    ####################################################################################################################
    def normalization(self, data, M_o, m_o, M, m):
        """Normalization (Min-Max Feature scaling)

        Args:
            data: feature
            M_o: data max
            m_o: data min
            M: normalization max
            m: normalization min

        Returns:
            Normalized feature
        """
        return (data - m_o)/(M_o - m_o) * (M-m) + m
    ####################################################################################################################

    ####################################################################################################################
    def training(self):
        """SVM model training and test

        Returns:
            SVM model
        """
        ################################################################################################################
        # feature extraction
        [HR_n, RR_n, pe_n] = self.feature_ext(self.ppg_N_set['subject' + str(self.sub_num)], 0)
        [HR_d, RR_d, pe_d] = self.feature_ext(self.ppg_D_set['subject' + str(self.sub_num)], 0)

        ################################################################################################################
        # Segmentation and average
        L_n = pe_n.shape[1]  # Length for average of normal
        L_d = pe_d.shape[1]  # Length for average of drowsiness

        HR_n_t = np.transpose(preprocessing.average(HR_n, L_n))
        HR_n_t = self.normalization(HR_n_t, 120, 50, 1, 0)
        RR_n_t = np.transpose(preprocessing.average(RR_n, L_n))
        RR_n_t = self.normalization(RR_n_t, 2, 0.5, 1, 0)
        pe_n_t = np.transpose(pe_n)

        HR_d_t = np.transpose(preprocessing.average(HR_d, L_d))
        HR_d_t = self.normalization(HR_d_t, 120, 50, 1, 0)
        RR_d_t = np.transpose(preprocessing.average(RR_d, L_d))
        RR_d_t = self.normalization(RR_d_t, 2, 0.5, 1, 0)
        pe_d_t = np.transpose(pe_d)

        L_n = np.min([L_n, len(HR_n_t), len(RR_n_t)])
        L_d = np.min([L_d, len(HR_d_t), len(RR_d_t)])

        X = np.zeros((L_n+L_d, 3))
        X[:L_n, 0:1] = HR_n_t[:L_n, :]
        X[L_n:, 0:1] = HR_d_t[:L_d, :]
        X[:L_n, 1:2] = RR_n_t[:L_n, :]
        X[L_n:, 1:2] = RR_d_t[:L_d, :]
        X[:L_n, 2:3] = pe_n_t[:L_n, :]
        X[L_n:, 2:3] = pe_d_t[:L_d, :]
        
        Y = np.ones((L_n+L_d, 1))
        Y = Y.ravel((len(Y), 0))
        Y[L_n:] = 0

        ################################################################################################################
        # SVM model
        # svm_model = SVC(kernel='linear', C=1.0, random_state=0).fit(X, Y)
        svm_model = SVC(kernel='rbf', C=1.0, gamma=2).fit(X, Y)

        ################################################################################################################
        # 5-fold cross validation
        acc = []
        cv = KFold(5, shuffle=True, random_state=0)
        for i, (idx_train, idx_test) in enumerate(cv.split(X)):
            input_x = X[idx_train]
            input_y = Y[idx_train]
            test_x = X[idx_test]
            test_y = Y[idx_test]

            # svm_model_test = SVC(kernel='linear', C=1.0, random_state=0).fit(input_x, input_y)
            svm_model_test = SVC(kernel='rbf', C=1.0, gamma=5).fit(input_x, input_y)

            pre = svm_model_test.predict(test_x)
            acc.append(len([i for i in range(len(pre)) if pre[i] == test_y[i]])/len(pre))
            print('%.3f' % (acc[i]))

        print('Average accuracy: %.3f' % (np.average(acc)))

        return svm_model

# if __name__ == '__main__':
#     training_class = process_class(1)
#     model = training_class.training()