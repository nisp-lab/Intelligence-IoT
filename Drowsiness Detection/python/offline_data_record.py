"""
Implicit emotional state recognition technology based on physiological signal
(SW for user status (drowsiness, concentration,...) classification using heart rate information)

Code Description:
    Socket communication with Android application for acquisition of individual users' PPG data using PPG measurement equipment (Empatica E4)
    Recording PPG data

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
import csv
import datetime


def run_server(port=9999, host=''):
    """Read PPG data and write to CSV file

    Args:
       port: port number
       host: IP
    """
    # socket connection with android code
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        client_socket_em, addr_em = server_socket.accept()
        print('PPG socket connect')
        dt = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        ppg_set = []

        # total 30 minutes
        for ii in range(0, 30):
            for i in range(0, 60):
                data = client_socket_em.recv(1024).decode("utf-8", "ignore")
                ppg = data.replace('[', '').replace(']', '').replace('\n', ',').split(',')
                print(ppg)
                ppg_set += ppg

            # PPG data recording
            # - Written as a line every 60 seconds
            with open('./record/' + dt + '.csv', 'a', encoding='utf-8', newline='') as f:
                wr = csv.writer(f)
                wr.writerow(ppg_set)
                ppg_set.clear()


if __name__ == '__main__':
    run_server()
