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

It is the main code for the online experiment and it is the code that makes the SSVEP stimulus.
TCP processes is executed through threads.

Check parameter initial value.

"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

import time

import threading
import online_Tcpip


class Stimulus:
    
    def __init__(self):
        
        
        self.count = 0
        self.yescount=0
        
        self.c = []
        self.result = [0,0]
        self.Time = [0]
    
    def start(self):
        #tcp thread
        d = online_Tcpip.biosemi()
        t_data = threading.Thread(target=d.biosemi_connect, args = ())
        t_data.start()
        
        self.c = d.check
        self.b = d.stim_after
        self.Time = d.Time
        self.result = d.result
        
        


        logging.console.setLevel(logging.WARNING)
        endExpNow = False  # flag for 'escape' or other condition => quit the exp
        expInfo = {}
        # Start Code - component code to be run before the window creation
 
        # Setup the Window
        win = visual.Window(
            size=[1060, 600], fullscr=True, screen=1,
            allowGUI=True, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            blendMode='avg', useFBO=True)
        # store frame rate of monitor if we can measure it
        expInfo['frameRate'] = win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        
        # Initialize components for Routine "setting"
        settingClock = core.Clock()
        def color_for_frame(herz,incolor=[-1,-1,-1]):
          period = 60/herz
        
          color = incolor
        
          if frameN % period < 0.5*period:
            color = [1,1,1]
          return color
        
        
        def highlight(which_button):
          if which_button != button:
            return [0,0,0]
          else:
            color = [-1,1,-1]
            if frameN > 30:
              color = [0,0,0]
            return color
        
        nTrial=4
        # blinky square settings
        low_x = -0.7
        hi_x  =  0.7
        low_y = -0.7
        hi_y  =  0.7
        center_y = 0
        center_x = 0
        blinky_size = [0.5, 0.5]
        width=blinky_size[0]
        height=blinky_size[1]
        text_offset = 0.3
       
        # global time
        
        global stimlabel
        stimlabel=np.array([0,0,0])
        global target
        target=0
        text_5 = visual.TextStim(win=win, name='text_5',
            text=None,
            font='Arial',
            pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-1.0);
        
        # Initialize components for Routine "welcome_message"
        welcome_messageClock = core.Clock()
        welcome = visual.TextStim(win=win, name='welcome',
            text='Welcome~',
            font='Arial',
            pos=(0, 0), height=0.4, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
        
        # Initialize components for Routine "blankscreen"
        blankscreenClock = core.Clock()
        text_7 = visual.TextStim(win=win, name='text_7',
            text=None,
            font='Arial',
            pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
        
        # Initialize components for Routine "focus"
        focusClock = core.Clock()
        text = visual.TextStim(win=win, name='text',
            text='Focus on monitor~!',
            font='Arial',
            pos=(0, 0), height=0.4, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
        
        
        # Initialize components for Routine "Device_stimulus"
        Device_stimulusClock = core.Clock()

        Device_label1 = visual.Rect(
            win=win, name='Device_label1',
            width=blinky_size[0], height=blinky_size[1],
            ori=0, pos=(low_x, center_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-1.0, interpolate=True)
        Device_label2 = visual.Rect(
            win=win, name='Device_label2',
            width=blinky_size[0], height=blinky_size[1],
            ori=0, pos=(hi_x, center_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-2.0, interpolate=True)

        
        Device_label1_text = visual.TextStim(win=win, name='Device_label1_text',
            text='Brightness',
            font='Arial',
            pos=(low_x, center_y+text_offset), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-3.0);
        Device_label2_text = visual.TextStim(win=win, name='Device_label2_text',
            text='Color',
            font='Arial',
            pos=(hi_x, center_y+text_offset), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-4.0);
        
                                      

        # Initialize components for Routine "Color_stimulus"
        Color_stimulusClock = core.Clock()

        Color_label1 = visual.Rect(
            win=win, name='Color_label1',
            width=blinky_size[0]-0.1, height=blinky_size[1]-0.1,
            ori=0, pos=(center_x, hi_y-0.1),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-1.0, interpolate=True)
        Color_label2 = visual.Rect(
            win=win, name='Color_label2',
            width=blinky_size[0]-0.1, height=blinky_size[1]-0.1,
            ori=0, pos=(hi_x, center_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-2.0, interpolate=True)
        Color_label3 = visual.Rect(
            win=win, name='Color_label3',
            width=blinky_size[0]-0.1, height=blinky_size[1]-0.1,
            ori=0, pos=(center_x, low_y-0.1),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-2.0, interpolate=True)
        Color_label4 = visual.Rect(
            win=win, name='Color_label4',
            width=blinky_size[0]-0.1, height=blinky_size[1]-0.1,
            ori=0, pos=(low_x, center_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-2.0, interpolate=True)
        
        Color_label1_text = visual.TextStim(win=win, name='Color_label1_text',
            text='Green',
            font='Arial',
            pos=(center_x, hi_y+text_offset-0.1), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-3.0);
        Color_label2_text = visual.TextStim(win=win, name='Color_label2_text',
            text='Blue',
            font='Arial',
            pos=(hi_x, center_y+text_offset), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-4.0);
        Color_label3_text = visual.TextStim(win=win, name='Color_label3_text',
            text='Off',
            font='Arial',
            pos=(center_x, low_y+text_offset-0.1), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-3.0);
        Color_label4_text = visual.TextStim(win=win, name='Color_label4_text',
            text='Red',
            font='Arial',
            pos=(low_x, center_y+text_offset), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-4.0);

             
      # Initialize components for Routine "Brightness_stimulus"
        Brightness_stimulusClock = core.Clock()

        Brightness_label1 = visual.ShapeStim(
            win=win, name='Brightness_label1',
            vertices=[[-(width, height)[0]/2.0,-(width, height)[1]/2.0], [+(width, height)[0]/2.0,-(width, height)[1]/2.0], [0,(width, height)[1]/2.0]],
            ori=0, pos=(center_x, hi_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-1.0, interpolate=True)
        
        Brightness_label2 = visual.ShapeStim(
            win=win, name='Brightness_label2',
            vertices=[[-(width, height)[0]/2.0,-(width, height)[1]/2.0], [+(width, height)[0]/2.0,-(width, height)[1]/2.0], [0,(width, height)[1]/2.0]],
            ori=180, pos=(center_x, low_y),
            lineWidth=1, lineColor=[0,0,0], lineColorSpace='rgb',
            fillColor=1.0, fillColorSpace='rgb',
            opacity=1, depth=-1.0, interpolate=True)

        Brightness_label1_text = visual.TextStim(win=win, name='Device_label1_text',
            text='Down',
            font='Arial',
            pos=(center_x+text_offset, low_y), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-3.0);
        Brightness_label2_text = visual.TextStim(win=win, name='Device_label2_text',
            text='Up',
            font='Arial',
            pos=(center_x+text_offset, hi_y), height=0.1, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=-4.0);
   
                                      
        
         # Initialize components for Routine "blankscreen"
        blankscreenClock = core.Clock()
        text_8 = visual.TextStim(win=win, name='text_8',
            text='Predict',
            font='Arial',
            pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
                                 
        # Initialize components for Routine "feedback"
        feedbackClock = core.Clock()
        feedbacktext = visual.TextStim(win=win, name='feedbacktext',
            text='Y or N',
            font='Arial',
            pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
        
        # Initialize components for Routine "end"
        endClock = core.Clock()
        text_6 = visual.TextStim(win=win, name='text_6',
            text='',
            font='Arial',
            pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
            color='black', colorSpace='rgb', opacity=1,
            depth=0.0);
        
        # Create some handy timers
        globalClock = core.Clock()  # to track the time since experiment started
        routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
        
        self.c[0] = 1
        start = time.time()
        
        print('====================GO=======================')
        # ------Prepare to start Routine "setting"-------
        t = 0
        settingClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(1.000000)
        start = time.time()
        self.b[0] = 0
        # update component parameters for each repeat
        
        # keep track of which components have finished
        settingComponents = [text_5]
        for thisComponent in settingComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "setting"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = settingClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *text_5* updates
            if t >= 0.0 and text_5.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_5.tStart = t
                text_5.frameNStart = frameN  # exact frame index
                text_5.setAutoDraw(True)
            frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
            if text_5.status == STARTED and t >= frameRemains:
                text_5.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in settingComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "setting"-------
        for thisComponent in settingComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        global_clock=core.Clock()
        end = time.time()
        self.Time[0] = end - start
        # ------Prepare to start Routine "welcome_message"-------
        t = 0
        welcome_messageClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(3.000000)
        start = time.time()
        self.b[0] = 3
        # update component parameters for each repeat
        # keep track of which components have finished
        welcome_messageComponents = [welcome]
        for thisComponent in welcome_messageComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "welcome_message"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = welcome_messageClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *welcome* updates
            if t >= 0.0 and welcome.status == NOT_STARTED:
                # keep track of start time/frame for later
                welcome.tStart = t
                welcome.frameNStart = frameN  # exact frame index
                welcome.setAutoDraw(True)
            frameRemains = 0.0 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
            if welcome.status == STARTED and t >= frameRemains:
                welcome.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in welcome_messageComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "welcome_message"-------
        for thisComponent in welcome_messageComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        end = time.time()
        self.Time[0] = end - start
        
        
        # set up handler to look after randomisation of conditions etc
        trials_2 = data.TrialHandler(nReps=nTrial, method='random', 
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='trials_2')
        thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
        if thisTrial_2 != None:
            for paramName in thisTrial_2:
                exec('{} = thisTrial_2[paramName]'.format(paramName))
        
        for thisTrial_2 in trials_2:
            currentLoop = trials_2
            # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
            if thisTrial_2 != None:
                for paramName in thisTrial_2:
                    exec('{} = thisTrial_2[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "blankscreen"-------
            t = 0
            blankscreenClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(1.000000)
            start = time.time()
            self.b[0] = 0
            # update component parameters for each repeat
            # keep track of which components have finished
            blankscreenComponents = [text_7]
            for thisComponent in blankscreenComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "blankscreen"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = blankscreenClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_7* updates
                if t >= 0.0 and text_7.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text_7.tStart = t
                    text_7.frameNStart = frameN  # exact frame index
                    text_7.setAutoDraw(True)
                frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text_7.status == STARTED and t >= frameRemains:
                    text_7.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in blankscreenComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "blankscreen"-------
            for thisComponent in blankscreenComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            end = time.time()
            self.Time[0] = end - start
            
            
            # ------Prepare to start Routine "focus"-------
            t = 0
            focusClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(3.000000)
            
            start = time.time()
            self.b[0] = 4
            
            # update component parameters for each repeat
            # keep track of which components have finished
            focusComponents = [text]
            for thisComponent in focusComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
                    
                    
            # -------Start Routine "focus"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = focusClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text* updates
                if t >= 0.0 and text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text.tStart = t
                    text.frameNStart = frameN  # exact frame index
                    text.setAutoDraw(True)
                frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text.status == STARTED and t >= frameRemains:
                    text.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in focusComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "focus"-------
            for thisComponent in focusComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            end = time.time()
            self.Time[0] = end - start
            


            # ------Prepare to start Routine "Device_stimulus"-------
            t = 0
            Device_stimulusClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(3.000000)
            
            self.result[1]=0
            start = time.time()
            self.b[0] = 1
            
            # update component parameters for each repeat
            
            # keep track of which components have finished
            # keep track of which components have finished
            Device_stimulusComponents = [Device_label1,Device_label2, Device_label1_text, Device_label2_text]
            for thisComponent in Device_stimulusComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "stimulus"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = Device_stimulusClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                figure1 = color_for_frame(5.45) # On
                figure2 = color_for_frame(12.0) # Off
                          
                
                
                # *Device_label1* updates
                if t >= 0.0 and Device_label1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Device_label1.tStart = t
                    Device_label1.frameNStart = frameN  # exact frame index
                    Device_label1.setAutoDraw(True)
                frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Device_label1.status == STARTED and t >= frameRemains:
                    Device_label1.setAutoDraw(False)
                if Device_label1.status == STARTED:  # only update if drawing
                    Device_label1.setFillColor(figure1, log=False)
                
                # *Device_label2* updates
                if t >= 0.0 and Device_label2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Device_label2.tStart = t
                    Device_label2.frameNStart = frameN  # exact frame index
                    Device_label2.setAutoDraw(True)
                frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Device_label2.status == STARTED and t >= frameRemains:
                    Device_label2.setAutoDraw(False)
                if Device_label2.status == STARTED:  # only update if drawing
                    Device_label2.setFillColor(figure2, log=False)
                          
                
                # *Device_label1_text* updates
                if t >= 0.0 and Device_label1_text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Device_label1_text.tStart = t
                    Device_label1_text.frameNStart = frameN  # exact frame index
                    Device_label1_text.setAutoDraw(True)
                frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Device_label1_text.status == STARTED and t >= frameRemains:
                    Device_label1_text.setAutoDraw(False)
                
                # *Device_label2_text* updates
                if t >= 0.0 and Device_label2_text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Device_label2_text.tStart = t
                    Device_label2_text.frameNStart = frameN  # exact frame index
                    Device_label2_text.setAutoDraw(True)
                frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Device_label2_text.status == STARTED and t >= frameRemains:
                    Device_label2_text.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Device_stimulusComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "stimulus"-------
            for thisComponent in Device_stimulusComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            end = time.time()
            self.Time[0] = end - start  
            
             # ------Prepare to start Routine "blankscreen"-------
            t = 0
            blankscreenClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(1.000000)
            start = time.time()
            self.b[0] = 0
            # update component parameters for each repeat
            # keep track of which components have finished
            blankscreenComponents = [text_7]
            for thisComponent in blankscreenComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            # -------Start Routine "blankscreen"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = blankscreenClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_7* updates
                if t >= 0.0 and text_7.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text_7.tStart = t
                    text_7.frameNStart = frameN  # exact frame index
                    text_7.setAutoDraw(True)
                frameRemains = 0.0 + 1.0- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text_7.status == STARTED and t >= frameRemains:
                    text_7.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in blankscreenComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "blankscreen"-------
            for thisComponent in blankscreenComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            end = time.time()
            self.Time[0] = end - start
            
            
            
            # ------Prepare to start Routine "focus"-------
            t = 0
            focusClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            routineTimer.add(3.000000)
            
            start = time.time()
            self.b[0] = 4
            
            # update component parameters for each repeat
            # keep track of which components have finished
            focusComponents = [text]
            for thisComponent in focusComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
              
            
            # -------Start Routine "focus"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = focusClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text* updates
                if t >= 0.0 and text.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text.tStart = t
                    text.frameNStart = frameN  # exact frame index
                    text.setAutoDraw(True)
                frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
                if text.status == STARTED and t >= frameRemains:
                    text.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in focusComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "focus"-------
            for thisComponent in focusComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            end = time.time()
            self.Time[0] = end - start
            
            #self.result[1]=1
            if self.result[1]==1:
                

                # ------Prepare to start Routine "Brightness_stimulus"-------
                t = 0
                Brightness_stimulusClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                routineTimer.add(3.000000)
                
                start = time.time()
                self.b[0] = 1
                print('bri')
                #self.result[1]=1
                # update component parameters for each repeat
                
                # keep track of which components have finished
                Brightness_stimulusComponents = [Brightness_label1,Brightness_label2, Brightness_label1_text, Brightness_label2_text]
                for thisComponent in Brightness_stimulusComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "Brightness_stimulus"-------
                while continueRoutine and routineTimer.getTime() > 0:
                    # get current time
                    t = Brightness_stimulusClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    figure1 = color_for_frame(5.45) # On
                    figure2 = color_for_frame(12.0) # Off
                              
                    
                    
                    # *Brightness_label1* updates
                    if t >= 0.0 and Brightness_label1.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Brightness_label1.tStart = t
                        Brightness_label1.frameNStart = frameN  # exact frame index
                        Brightness_label1.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Brightness_label1.status == STARTED and t >= frameRemains:
                        Brightness_label1.setAutoDraw(False)
                    if Brightness_label1.status == STARTED:  # only update if drawing
                        Brightness_label1.setFillColor(figure1, log=False)
                    
                    # *Brightness_label2* updates
                    if t >= 0.0 and Brightness_label2.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Brightness_label2.tStart = t
                        Brightness_label2.frameNStart = frameN  # exact frame index
                        Brightness_label2.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Brightness_label2.status == STARTED and t >= frameRemains:
                        Brightness_label2.setAutoDraw(False)
                    if Brightness_label2.status == STARTED:  # only update if drawing
                        Brightness_label2.setFillColor(figure2, log=False)
                              
                    
                    # *Brightness_label1_text* updates
                    if t >= 0.0 and Brightness_label1_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Brightness_label1_text.tStart = t
                        Brightness_label1_text.frameNStart = frameN  # exact frame index
                        Brightness_label1_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Brightness_label1_text.status == STARTED and t >= frameRemains:
                        Brightness_label1_text.setAutoDraw(False)
                    
                    # *Brightness_label2_text* updates
                    if t >= 0.0 and Brightness_label2_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Brightness_label2_text.tStart = t
                        Brightness_label2_text.frameNStart = frameN  # exact frame index
                        Brightness_label2_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Brightness_label2_text.status == STARTED and t >= frameRemains:
                        Brightness_label2_text.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in Brightness_stimulusComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "Brightness_stimulus"-------
                for thisComponent in Brightness_stimulusComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                
                end = time.time()
                self.Time[0] = end - start  
                
            else:

                # ------Prepare to start Routine "Color_stimulus"-------
                t = 0
                Color_stimulusClock.reset()  # clock
                frameN = -1
                continueRoutine = True
                routineTimer.add(3.000000)
                
                start = time.time()
                self.b[0] = 1
                print('color')
                #self.result[1]=2
                # update component parameters for each repeat
                
                # keep track of which components have finished
                # keep track of which components have finished
                Color_stimulusComponents = [Color_label1,Color_label2,Color_label3, Color_label4, Color_label1_text, Color_label2_text, Color_label3_text, Color_label4_text]
                for thisComponent in Color_stimulusComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED
                
                # -------Start Routine "Color_stimulus"-------
                while continueRoutine and routineTimer.getTime() > 0:
                    # get current time
                    t = Color_stimulusClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame
                    figure1 = color_for_frame(5.45,[-1,1,-1]) # Green(label1) 
                    figure2 = color_for_frame(12,[-1,-1,1]) # Blue(label2)
                    figure3 = color_for_frame(8.57) # Light off(label3)
                    figure4 = color_for_frame(15,[1,-1,-1]) # Red(label4)                  
                    
                    
                    # *Color_label1* updates
                    if t >= 0.0 and Color_label1.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label1.tStart = t
                        Color_label1.frameNStart = frameN  # exact frame index
                        Color_label1.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label1.status == STARTED and t >= frameRemains:
                        Color_label1.setAutoDraw(False)
                    if Color_label1.status == STARTED:  # only update if drawing
                        Color_label1.setFillColor(figure1, log=False)
                    
                    # *Color_label2* updates
                    if t >= 0.0 and Color_label2.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label2.tStart = t
                        Color_label2.frameNStart = frameN  # exact frame index
                        Color_label2.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label2.status == STARTED and t >= frameRemains:
                        Color_label2.setAutoDraw(False)
                    if Color_label2.status == STARTED:  # only update if drawing
                        Color_label2.setFillColor(figure2, log=False)
                        
                    # *Color_label3* updates
                    if t >= 0.0 and Color_label3.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label3.tStart = t
                        Color_label3.frameNStart = frameN  # exact frame index
                        Color_label3.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label3.status == STARTED and t >= frameRemains:
                        Color_label3.setAutoDraw(False)
                    if Color_label3.status == STARTED:  # only update if drawing
                        Color_label3.setFillColor(figure3, log=False)
    
                    # *Color_label4* updates
                    if t >= 0.0 and Color_label4.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label4.tStart = t
                        Color_label4.frameNStart = frameN  # exact frame index
                        Color_label4.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label4.status == STARTED and t >= frameRemains:
                        Color_label4.setAutoDraw(False)
                    if Color_label4.status == STARTED:  # only update if drawing
                        Color_label4.setFillColor(figure4, log=False)                        
                    
                    # *Color_label1_text* updates
                    if t >= 0.0 and Color_label1_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label1_text.tStart = t
                        Color_label1_text.frameNStart = frameN  # exact frame index
                        Color_label1_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label1_text.status == STARTED and t >= frameRemains:
                        Color_label1_text.setAutoDraw(False)
                    
                    # *Color_text_4* updates
                    if t >= 0.0 and Color_label2_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label2_text.tStart = t
                        Color_label2_text.frameNStart = frameN  # exact frame index
                        Color_label2_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label2_text.status == STARTED and t >= frameRemains:
                        Color_label2_text.setAutoDraw(False)
    
                    # *Color_label3_text* updates
                    if t >= 0.0 and Color_label3_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label3_text.tStart = t
                        Color_label3_text.frameNStart = frameN  # exact frame index
                        Color_label3_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label3_text.status == STARTED and t >= frameRemains:
                        Color_label3_text.setAutoDraw(False)
                    
                    # *Color_label4_text* updates
                    if t >= 0.0 and Color_label4_text.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Color_label4_text.tStart = t
                        Color_label4_text.frameNStart = frameN  # exact frame index
                        Color_label4_text.setAutoDraw(True)
                    frameRemains = 0.0 + 5- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Color_label4_text.status == STARTED and t >= frameRemains:
                        Color_label4_text.setAutoDraw(False)
                    
                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in Color_stimulusComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished
                    
                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()
                    
                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()
                
                # -------Ending Routine "Color_stimulus"-------
                for thisComponent in Color_stimulusComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                
                end = time.time()
                self.Time[0] = end - start  

            
        # completed 10 repeats of 'trials_2'
        
        
        # ------Prepare to start Routine "end"-------
        t = 0
        endClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        routineTimer.add(3.000000)
        
        start = time.time()
        self.b[0] = 3
        
        # update component parameters for each repeat
        # keep track of which components have finished
        endComponents = [text_6]
        for thisComponent in endComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        # -------Start Routine "end"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = endClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_6* updates
            if t >= 0.0 and text_6.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_6.tStart = t
                text_6.frameNStart = frameN  # exact frame index
                text_6.setAutoDraw(True)
            frameRemains = 0.0 + 3- win.monitorFramePeriod * 0.75  # most of one frame period left
            if text_6.status == STARTED and t >= frameRemains:
                text_6.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in endComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "end"-------
        for thisComponent in endComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        end = time.time()
        self.Time[0] = end - start
        self.c[0] = 2
        time.sleep(10)
        logging.flush()
        
        win.close()
        core.quit()
        
       
        
b=Stimulus()
b.start()