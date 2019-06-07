"""
Implicit emotional state recognition technology based on physiological signal
(SW for user status (drowsiness, concentration,...) classification using heart rate information)

Code Description:
    Classifier model (SVM) training using acquired PPG data (realtime)
    Binary classification (awakening and drowsiness)

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

import socket
import threading
import numpy as np
import overall_process
import preprocessing
from phue import Bridge
import requests
from rgbxy import Converter
import phue

########################################################################################################################
# Connection with phue
res = requests.get('https://www.meethue.com/api/nupnp')
devices = res.json()
device_ip = devices[0]['internalipaddress']

try:
    b = Bridge(device_ip)
except phue.PhueRegistrationException:
    input("press link button in 30 seconds and enter..")
    b = Bridge(device_ip)
converter = Converter()
b.connect()
power = False
b.set_light(5, 'on', power)
########################################################################################################################

def run_server(port=9999, host=''):
    """Read PPG data

    Args:
       port: port number
       host: IP
    """
    # socket connection with android code
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        client_socket_em, addr_em = server_socket.accept()
        print('PPG Socket connect')
        ppg_set = []

        for ii in range(0, 120):
            for i in range(0, 60):
                data = client_socket_em.recv(1024).decode("utf-8", "ignore")
                ppg = data.replace('[', '').replace(']', '').replace('\n', ',').split(',')
                ppg_set += ppg

            # run thread for prediction per 30 seconds
            t = threading.Thread(target=threadwork_m, args=[ppg_set, client_socket_em])
            t.start()
            ppg_set.clear()

        client_socket_em.close()

    
def threadwork_m(bvp, soc):
    """Prediction using SVM

    Args:
       bvp: PPG data
       soc: socket
    """
    data = bvp
    # feature extraction
    [HR_test, RR_test, pe_test] = training_class.feature_ext(data, 1)

    # segmentation and averaging
    L_avg = pe_test.shape[1]

    HR_test = training_class.normalization(np.transpose(preprocessing.average(HR_test, L_avg)), 120, 50, 1, 0)
    RR_test = training_class.normalization(np.transpose(preprocessing.average(RR_test, L_avg)), 2, 0.5, 1, 0)
    pe_test = np.transpose(pe_test)

    L = min((L_avg, np.shape(HR_test)[0], np.shape(RR_test)[0]))

    X = np.zeros((L, 3))
    X[:, 0:1] = HR_test[:L, :]
    X[:, 1:2] = RR_test[:L, :]
    X[:, 2:3] = pe_test[:L, :]

    # prediction
    pre = model.predict(X)

    # When 70% of drowsiness is predicted, it is judged to be drowsy
    # If it is judged to be drowsy, turn off the light, and in the opposite case turn on the light
    D = [i for i in pre if i == 0]
    if len(D)/len(pre) >= 0.7:
        print('Drowsiness!!')
        b.set_light(5, 'on', False)
    else:
        print('Awakening..')
        b.set_light(5, 'on', True)


if __name__ == '__main__':
    # number of subject
    sub_num = 2
    # SVM model training
    training_class = overall_process.process_class(sub_num)
    model = training_class.training()
    run_server()