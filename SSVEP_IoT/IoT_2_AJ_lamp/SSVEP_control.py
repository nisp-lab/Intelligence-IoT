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

Control the Alljoyn Lamp through the analyzed EEG.
1. On/Off control
2. Brightness control
3. Color control (blue, red, green)

"""

import threading
import numpy as np
import time
import requests
import classification_4class
import classification_2class

class process():
    
    def __init__(self, stack,stim,check,time,sample_count,slice_check,result):
        
        self.highcut = 50
        self.fs = 256
        self.stack = stack
        
        self.check = check
        self.slice_check = slice_check 
        self.Time = time
        self.result = result
        
        self.label = {}
        self.label['target']=[]
        
        self.after = stim
        self.before = [0]
        
        
        self.sample_count = sample_count

        self.channel = 32                    
        self.count = 0
        self.flag = 0
        self.data = np.zeros((1,9))
        self.filt_to_data = np.zeros((64, 9))

        self.cf = classification_4class.class_feature()
        self.cf2 = classification_2class.class_feature()
        
        
        
        self.color=['50','100','30','0'] #g=50 b=100 off=30 r=0
        
        
        
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
                        
                        data = self.arrange_data(self.stack[0])
                        
                        
                        if self.result[1] == 0 :
                            self.result[0] = self.cf2.nispsvm(data)
                            self.result[1] = self.result[0]
                            
                            url = "http://128.134.65.120:7579/Mobius/kwu-hub/AJ-Lamp/Power"
                            payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<m2m:cin xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <con>"\
                            "on</con>\n</m2m:cin>"
                            
                            
                        elif self.result[1] == 1:
                            
                            self.result[0] = self.cf2.nispsvm(data)
                            
                            url = "http://128.134.65.120:7579/Mobius/kwu-hub/AJ-Lamp/Brightness"
                            response = requests.request("GET", url+"/latest", headers=self.headers)
                            response11=response.text
                            before = response11[response11.index('<con>')+5:response11.index('</con>')]
                            print(before)
                            if before=='on':
                                after = 50
                            else:
                                after = int(int(before) + 50*(-1)**(self.result[0]+1) )
                                
                            if after<1:
                                after=1
                            elif after>100:
                                after=100
                           
                            payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<m2m:cin xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <con>"\
                            +str(after)+"</con>\n</m2m:cin>"
                            
                            print('result = ',after)
                                
                            

                        else:
                            
                            self.result[0] = self.cf.nispsvm(data)
                            print('rererere = ',self.result[0])
                            
                            
 
                            if self.result[0] == 3:
                                url = "http://128.134.65.120:7579/Mobius/kwu-hub/AJ-Lamp/Power"
                                payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<m2m:cin xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <con>off</con>\n</m2m:cin>"
                                
                            else :
                                url = "http://128.134.65.120:7579/Mobius/kwu-hub/AJ-Lamp/Color"
                                payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<m2m:cin xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n    <con>"\
                                +self.color[int(self.result[0])-1]+"</con>\n</m2m:cin>"
                                
                            print('result = ',self.color[int(self.result[0])-1])
                        response = requests.request("POST", url, data=payload, headers=self.headers)
                        
                        
                        
                            
                    self.slice_check[0] = 0
                    
                self.Time[0]=0
                
                
            # stimulus end
            if self.check[0] == 2 :
                print(self.before)
                break

            
    
    
    
    
    
