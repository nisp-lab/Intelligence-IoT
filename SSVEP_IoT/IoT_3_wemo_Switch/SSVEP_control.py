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

Control the Wemo_switch through the analyzed EEG.
1. On/Off control

"""
import threading
import numpy as np
import time
import pandas as pd
import requests
import classification_2class

class process():
    
    def __init__(self, stack,stim,check,time,sample_count,slice_check):
        
        self.fs = 256
        self.channel = 32   
        self.stack = stack
        
        self.check = check
        self.slice_check = slice_check 
        self.Time = time
        
        self.label = {}
        self.label['target']=[]
        
        self.after = stim
        self.before = [0]
        self.sample_count = sample_count

        self.cf = classification_2class.class_feature()
       
        self.url = "http://128.134.65.120:7579/Mobius/kwu-hub/WeMo-Switch/Power"
        self.headers = {
            'Accept': "application/xml",
            'X-M2M-RI': "12345",
            'X-M2M-Origin': "/0.2.481.1.21160310105204806",
            'Content-Type': "application/vnd.onem2m-res+xml; ty=4",
            'Cache-Control': "no-cache",
            'Postman-Token': "414ff19c-23cd-44d8-949c-dbc7b39ea63a"
            }
       
        
        t_pre = threading.Thread(target  = self.extract_data, args = ())
        t_pre.start()
        
    def arrange_data(self,Indata):
       
        data = np.zeros((len(Indata['ch1']),self.channel))
        for i in range(self.channel):
            data[:,i] = np.array(Indata['ch'+str(i+1)])
            
        return data
                    
    def extract_data(self):
        count = 0
        # wait for stimulus setting
        while 1:            
            time.sleep(0.0001)            
            if self.check[0] == 1 :
                break 
        
        while 1 :
                        
            if self.before[-1] != self.after[0]:
                self.before.append(self.after[0])
                
   
            time.sleep(0.0001)  
            if self.Time[0] != 0:

                if count < len(self.before)-1:
                    count += 1

                self.label['target'] += [self.before[count] for i in range(round(self.Time[0])*self.fs)]
                self.sample_count[0] = round(self.Time[0])*self.fs
                
                if (self.slice_check[0] == 1):
                    if (self.before[count-1] == 1) :
                        print('label =',self.before[count-1])
                        data = self.arrange_data(self.stack[0])
                        result = self.cf.nispsvm(data)
                        
                        if result == 1:
                            #self.power = not self.power
                            control = 'on'
                        else :
                            control = 'off'
                            
                        payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<m2m:cin xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <con>"\
                        +control+"</con>\n</m2m:cin>"

                        response = requests.request("POST", self.url, data=payload, headers=self.headers)
                        print('result = ',result)
  
                    self.slice_check[0] = 0
                    
                self.Time[0]=0

            # stimulus end
            if self.check[0] == 2 :
                print(self.before)
                break


            
    
    
    
    
    
