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

Data is loaded in real time by TCP/IP connection with BioSemi.

Check the port number and buffer size of BioSemi.

Run the analysis process through threads to perform real-time analysis.

"""


import socket                    # used for TCP/IP communication
import time
import SSVEP_control

class biosemi():
    
    def __init__(self):
        self.stack = {}       # data storage
        self.full ={}
        self.temp =[0]
        self.slice_stack={}
        for i in range(1, 33):
            self.stack['ch' + str(i)] = []  #Data received by TCP
            self.slice_stack['ch' + str(i)] = []   #slice data
            self.full['ch' + str(i)] = []   
        
        self.check = [0]
        self.stim_after = [0]
        self.Time=[0]
        self.sample_count=[0]   # Number of samples for that stimulus ( ex if stimulus time is 3 sec,sample_count= samplerate * 3)
        self.slice_check=[0] # Data slice completion check corresponding to visual stimulus
        self.result=[0,0]
        self.channel=32
        #self.process = test_bci.process(self.temp,self.stim_after,self.check,self.Time,self.sample_count,self.slice_check)
        self.process = SSVEP_control.process(self.temp,self.stim_after,self.check,self.Time,self.sample_count,self.slice_check,self.result)

    def biosemi_connect(self):
        
        # TCP/IP setup
        TCP_IP = '127.0.0.1' # ActiView is running on the same PC
        TCP_PORT = 8888       # This is the port ActiView listens on
        BUFFER_SIZE = 192    # Data packet size (depends on ActiView settings)
       
        # if the psychopy tool is intialized, biosemi device and tcpip communication is started
     
        while 1:            
            time.sleep(0.0001)            
            if self.check[0] == 1 :
                start = time.time()
                
                break  
        # Open socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        
        a=0
        # Calculate spectrum 50 times
        while 1:
            # Parse incoming frame data
            time.sleep(0.00001)  
            
            # collect 32 packets to fill the window
           
            # Read the next packet from the network
            data = s.recv(BUFFER_SIZE)
            

        
            # Extract 2 channel 1 samples from the packet
            for k in range(2):

                for m in range(self.channel): 
                    
                    offset = m * 3 + int(BUFFER_SIZE/2) * k
                    # The 3 bytes of each sample arrive in reverse order
                    
                    z=(data[offset+2]>>7)
                    if z ==1:
                        sample = ((data[offset+2]) << 16)
                        sample += ((data[offset+1]) << 8)
                        sample += (data[offset])
                        sample -= 2*(z<<23)
                    else:
                        sample = ((data[offset+2]) << 16)
                        sample += ((data[offset+1]) << 8)
                        sample += (data[offset])

                    # Store all ch's samples
                    sample= sample*0.03125
                    self.stack['ch' + str(m+1)].append(sample)
                    self.full['ch' + str(m+1)].append(sample)

                # slice data
                if self.sample_count[0] != 0:
                    if (self.sample_count[0] < len(self.stack['ch'+str(self.channel)])) & (self.slice_check[0]==0) : 
                    
                        for j in range(self.channel):
                            self.slice_stack['ch' + str(j+1)] = self.stack['ch' + str(j+1)][:self.sample_count[0]]
                            self.stack['ch' + str(j+1)][:]=self.stack['ch' + str(j+1)][self.sample_count[0]:]
                            
                        self.slice_stack = {'ch'+str(i): self.slice_stack['ch'+str(i)][:] for i in range(1, len(self.slice_stack)+1)}
                        self.temp[0]=self.slice_stack
                        self.slice_check[0] =1
                        self.sample_count[0]=0
                
            
            if self.check[0] == 2 :
                if a==0:
                    end = time.time()
                    a=1
                
                if len(self.stack['ch' + str(m+1)]) > (end - start) * 256 + 1:
                    break
            
        

         #Close socket
        s.close()
