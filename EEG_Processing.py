#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy import signal
import socket

##########################
# More information about EEG analysis
# https://github.com/curiositry/EEGrunt
##########################


class EEG_Processing:
    
    def __init__(self, path, filename):

        self.path = path
        self.filename = filename

    def load_file(self):

        path = self.path
        filename = self.filename

        print("Loading EEG data: "+path+filename)

        try:
            with open(path+filename) as file:
                pass

        except IOError:
            print 'EEG data file not found.'
            exit()

        # Columns from 0-8 content the channels information and the frequency sample
        columns = (0,1,2,3,4,5,6,7,8)
        # The first 6 lines are just comments and the 2s next are just from the initial clue
        skiprows = 506

        # Load the data using loadtxt to fast reader
        raw_data = np.loadtxt(path + filename,
                              delimiter=',',
                              skiprows=skiprows,
                              usecols=columns)

        self.raw_data = raw_data

        self.fs_Hz = 250.0

        # Calculate the time using the samples data
        # [ first_row:last_row , column_0 ]
        self.t_sec = np.arange(len(self.raw_data[:, 0])) / self.fs_Hz

        #print "Session lenght (seconds): "+str(len(self.t_sec)/self.fs_Hz)
        #print "t_sec last: "+str(self.t_sec[:-1])
        #print "Lenght raw data: " + str(len(self.raw_data))
        #print "Session lenght (seconds): "+str(len(self.t_sec))

        self.nchannels = 8
        self.channels = [1,2,3,4,5,6,7,8]


        # Even channels
        self.evenchannels = [2,4,6,8]
        # Odd channels
        self.oddchannels = [1,3,5,7]

        # NEEEWWW
        self.NFFT = 512

        self.sample_block = 11

        self.plot = 'save'

        self.overlap  = self.NFFT - int(0.25 * self.fs_Hz)

        self.ecg_threshold_factor = 6
        self.hrv_window_length = 10
        

    def load_channel(self, channel):

        print("Loading channel: "+str(channel))
        channel_data = self.raw_data[:,(channel)]
        self.channel = channel
        self.data = channel_data
        
        
    def map_channel(self, channel):
    
        if str (channel) == "1":
            m_channel = "FCC3h"
            print ("Channel Map: " + str(m_channel))
            
        if str(channel) == "2":
            m_channel = "FCC4h"
            print ("Channel Map: " + str(m_channel))
            
        if str(channel) == "3":
            m_channel = "FCC5h"
            print ("Channel Map: " + str(m_channel))
         
        if  str(channel) == "4":
            m_channel = "FCC6h"
            print ("Channel Map: " + str(m_channel))
             
        if str (channel) == "5":
            m_channel = "CCP3h"
            print ("Channel Map: " + str(m_channel))
             
        if str(channel) == "6":
            m_channel = "CCP4h"
            print ("Channel Map: " + str(m_channel))
        
        if str(channel) == "7":
            m_channel = "CCP5h"
            print ("Channel Map: " + str(m_channel))
        
        if  str(channel) == "8":
            m_channel = "CCP6h"
            print ("Channel Map: " + str(m_channel))
        
       
        self.m_channel = m_channel

    def remove_dc_offset(self):

        hp_cutoff_Hz = 1.0

        #print("Highpass filtering at: " + str(hp_cutoff_Hz) + " Hz")

        #nyquist_freq = (self.fs_Hz / 2.0)
        
        b, a = signal.butter(2, hp_cutoff_Hz/(self.fs_Hz / 2.0), 'highpass')
        self.data = signal.lfilter(b, a, self.data, 0)

    def notch_mains_interference(self):
        notch_freq_Hz = np.array([60.0])  # main + harmonic frequencies
        for freq_Hz in np.nditer(notch_freq_Hz):  # loop over each target freq
            bp_stop_Hz = freq_Hz + 3.0*np.array([-1, 1])  # set the stop band
            b, a = signal.butter(3, bp_stop_Hz/(self.fs_Hz / 2.0), 'bandstop')
            self.data = signal.lfilter(b, a, self.data, 0)
            #print("Notch filter removing: " + str(bp_stop_Hz[0]) + "-" + str(bp_stop_Hz[1]) + " Hz")


    def bandpass(self,start,stop):
        bp_Hz = np.zeros(0)
        bp_Hz = np.array([start,stop])
        b, a = signal.butter(3, bp_Hz/(self.fs_Hz / 2.0),'bandpass')
        #print("Bandpass filtering to: " + str(bp_Hz[0]) + "-" + str(bp_Hz[1]) + " Hz")
        return signal.lfilter(b, a, self.data, 0)

    # 250 * n = t
    #def segment(self, N, P, channel):
    def segment(self, channel):

        print("Generating signal plot...")
        plt.figure(figsize=(10,5))
        plt.subplot(1,1,1)
        #plt.plot(self.t_sec[N:P],self.data[N:P])
        plt.plot(self.t_sec,self.data)
        plt.xlabel("Tiempo (segundos)")
        plt.ylabel("Amplitud (uV)")
        plt.title("Signal: " + str(channel))
        plt.draw
        
        
        
    def signal_plot(self, channel):

        print("Generating signal plot...")
        plt.figure(figsize=(10,5))
        plt.subplot(1,1,1)
        plt.plot(self.t_sec,self.data, label="Canal" +str(self.m_channel))
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud (uV)")
        plt.legend()
        plt.title(r'Banda mu de la se$\tilde{n}$al EEG')
        plt.draw()
        plt.show()        

    def plot_fft(self,channel):
        
        voltage = self.data/(self.data.max()) # normalize the values
        magnitude = np.fft.rfft(voltage)
        freq = np.fft.rfftfreq(len(self.t_sec),np.diff(self.t_sec)[0])
        #plt.figure()
        #plt.plot(freq, np.absolute(magnitude), lw = 1)
        #plt.ylim(0,100)
        #plt.xlim(0,100)
        
        plt.figure(figsize=(10,5))
        plt.subplot(1,1,1)
        plt.plot(freq,np.absolute(magnitude), lw = 1, label="Canal" +str(self.m_channel))
        plt.xlabel("Frecuencia (Hz)")
        plt.ylabel("Magnitud |E(f)|")
        plt.legend()
        plt.title(r'Transformada R$\acute{a}$pida de Fourier sobre la banda mu de la se$\tilde{n}$al EEG ')
        plt.draw()
        plt.show()        
        

    def get_spectrum_data(self):
        #print("Calculating spectrum data...")
        self.spec_PSDperHz, self.spec_freqs, self.spec_t = mlab.specgram(np.squeeze(self.data),
                                       NFFT=self.NFFT,
                                       window=mlab.window_hanning,
                                       Fs=self.fs_Hz,
                                       noverlap=self.overlap
                                       ) # returns PSD power per Hz
        # convert the units of the spectral data
        self.spec_PSDperBin = self.spec_PSDperHz * self.fs_Hz / float(self.NFFT)
    

    def plot_band_power(self,start_freq,end_freq,band_name, channel):
        #print("Plotting band power over time. Frequency range: "+str(start_freq)+" - "+str(end_freq))
        bool_inds = (self.spec_freqs > start_freq) & (self.spec_freqs < end_freq)
        band_power = np.sqrt(np.amax(self.spec_PSDperBin[bool_inds, :], 0))
        self.band_power = band_power
        #plt.figure(figsize=(10,5))
        #plt.plot(self.spec_t,band_power)
        #plt.ylim([np.amin(band_power), np.amax(band_power)+1])
        # plt.xlim(len(x)/config['sample_block'])
        #plt.xlabel('Tiempo (s)')
        #plt.ylabel(r'Amplitud se$\tilde{n}$al EEG (uVrms)')
        #plt.title('Trend Graph of '+band_name+' EEG Amplitude over Time' +str(channel)) 
        #plt.draw()
       # plt.show()
        
        
    def erd_cal(self, channel,N,P):
        
        #Need to extract the time for each task
        
        #plt.figure(figsize=(10,5))
        #plt.plot(self.spec_t[N:P],self.band_power[N:P], lw = 1, label="Canal" +str(self.m_channel))
        #plt.ylim([np.amin(self.band_power), np.amax(self.band_power)+1])
        #plt.xlabel('Time (sec)')
        #plt.ylabel('EEG Amplitude (uVrms)')
        #plt.legend()
        #plt.title(r'Banda mu de la se$\tilde{n}$al EEG')
        #plt.draw()
        #plt.show()
        
        I = 5
        F = 8
        plt.figure(figsize=(10,5))
        plt.plot(self.spec_t[I:F],self.band_power[I:F], lw = 1, label="Canal" +str(self.m_channel))
        plt.ylim([np.amin(self.band_power), np.amax(self.band_power)+1])
        # plt.xlim(len(x)/config['sample_block'])
        plt.xlabel('Time (sec)')
        plt.ylabel('EEG Amplitude (uVrms)')
        plt.legend()
        plt.title(r'Banda mu de la se$\tilde{n}$al EEG')
        plt.draw()
        plt.show()
        
        ######## AVG #########
            
        #A = np.average(self.band_power[N:P] )
        #E = np.average(self.band_power[5:8] )
        
        R = np.mean(self.band_power[I:F] ) # Mean value in the rest 
        
        #AE = self.band_power[12:60] - E
        
        #AEA = np.amin(abs(AE))
        A = np.amin(self.band_power[N:P])
        #AEAE = np.amax(abs(AE))
        
        #np.average(data)
        
        #min =  np . amin (self.band_power[12:60] )
        #min = np.amin(A)
        #max =  np . amax(R )
        #self.min = min
        #self.max = max
        
        #print("Minimo" + str(min)) 
        #print("Maximo" + str(max)) 
    
        #erd = abs(((self.min - self.max)/self.max)*100)
        #erd = abs((A - E)/E*100)
        
        erd = abs((A - R)/R*100)
        print("ERD %: " + str(erd))
        print("A= " + str(A))
        return erd
        
    def avg(self, sum):
    
        avg = (sum/4)
        
        return avg
        
    def classify(self, avg_even, avg_odd):
 
        newIP = "127.0.0.1"
        #s = socket . socket ()
        #s.connect (( newIP , 9999) )
    
        if avg_even > avg_odd:
        
            print("Left hand")
            #s.send('3')
            
        else: 
            print("Right hand")
            #s.send('1')
            
        
        #s.close()
