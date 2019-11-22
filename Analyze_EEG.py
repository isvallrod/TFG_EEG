import EEG_Processing
import socket
    
path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Carlos/'
filename = 'OpenBCI-RAW-2019-06-17_16-32-21_I_Videito.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Luis/'
#filename = 'OpenBCI-RAW-2019-06-19_16-41-44_Videito.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Luis_2/'
#filename = 'OpenBCI-RAW-2019-06-17_17-13-11_R_Videito.txt'

#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A1/'
#filename = 'OpenBCI-RAW-2019-06-17_14-55-57_I_VI1.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A3/'
#filename = 'OpenBCI-RAW-2019-06-19_15-27-31_VID1.txt'

#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A2/'
#filename = 'OpenBCI-RAW-2019-06-19_15-38-40_VID2_6m.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Carlos/'
#filename = 'OpenBCI-RAW-2019-06-17_16-13-19_VI2_R.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Irene_2/'
#filename = 'OpenBCI-RAW-2019-06-19_17-30-17_VID2_Error_8m.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Luis/'
#filename = 'OpenBCI-RAW-2019-06-19_16-52-05_VID2.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Stef/'
#filename = 'OpenBCI-RAW-2019-06-19_13-49-43_VID2.txt'


#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A3/'
#filename = 'OpenBCI-RAW-2019-06-12_15-57-18_RI.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Irene/'
#filename = 'OpenBCI-RAW-2019-06-12_15-32-35_Real.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Irene/'
#filename = 'OpenBCI-RAW-2019-06-12_15-46-32_Im.txt'

#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A1/'
#filename = 'OpenBCI-RAW-2019-06-17_14-41-43_R_VI5.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Irene_2/'
#filename = 'OpenBCI-RAW-2019-06-19_17-41-49_VID5_Error_min8_9.txt'

#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Jesus/'
#filename = 'OpenBCI-RAW-2019-06-17_14-02-27_I_VI4.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Luis_2/'
#filename = 'OpenBCI-RAW-2019-06-17_17-34-25_I_VID4.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/A2/'
#filename = 'OpenBCI-RAW-2019-06-19_15-53-22_VID3.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Jesus/'
#filename = 'OpenBCI-RAW-2019-06-17_13-33-55_R_VI3.txt'
#path = '/home/isabelvr/Documents/IIS_2018/Proyecto/Proyecto_De_Graduacion/Mediciones_2/Stef/'
#filename = 'OpenBCI-RAW-2019-06-19_14-00-43_VID3.txt'       




# Initialize
EEG = EEG_Processing.EEG_Processing(path, filename)


# Load the EEG data
EEG.load_file()

#for channel in EEG.channels:

    #EEG.load_channel(channel)
    
    #EEG.remove_dc_offset()

#N = 8750
#P = 11250

N = 12
P = 60
SUM_E =0
SUM_O =0



for evenchannel in EEG.evenchannels:

        EEG.load_channel(evenchannel)
        EEG.map_channel(evenchannel)
        #EEG.plot_fft(evenchannel)
        #EEG.signal_plot(evenchannel)
        #EEG.segment(evenchannel)
        EEG.remove_dc_offset()
        EEG.notch_mains_interference()
        #EEG.signal_plot(evenchannel)
        #EEG.plot_fft(evenchannel)
        start_Hz = 8
        stop_Hz = 12
        EEG.data = EEG.bandpass(start_Hz,stop_Hz)
        #EEG.signal_plot(evenchannel)
        #EEG.plot_fft()
        EEG.get_spectrum_data()
        EEG.plot_band_power(8,12,"Alpha", evenchannel)
        #EEG.signal_plot(evenchannel)
        #EEG.plot_fft(evenchannel)
        p_erd =  EEG.erd_cal( evenchannel,N,P)
        SUM_E+= p_erd
        print("P_erd"+str(SUM_E))
       
        #EEG.segment(N,P,evenchannel)
        #EEG.segment(evenchannel)
        
avg_e = EEG.avg(SUM_E)
print("AVG"+str(avg_e))

for oddchannel in EEG.oddchannels:

        EEG.load_channel(oddchannel)
        EEG.map_channel(oddchannel)
        #EEG.plot_fft(oddchannel)
        #EEG.signal_plot(oddchannel)
        #EEG.signal_plot(oddchannel)
        EEG.remove_dc_offset()
        EEG.notch_mains_interference()
        #EEG.signal_plot(oddchannel)
        #EEG.plot_fft(oddchannel)
        start_Hz = 8
        stop_Hz = 12
        EEG.data = EEG.bandpass(start_Hz,stop_Hz)
        #EEG.signal_plot(oddchannel)        
        #EEG.plot_fft()
        EEG.get_spectrum_data()
        EEG.plot_band_power(8,12,"Aplha", oddchannel)
        #EEG.plot_fft(oddchannel)
        #EEG.signal_plot(oddchannel)
        o_erd =  EEG.erd_cal( oddchannel,N,P)
        SUM_O+= o_erd
        print("P_erd"+str(SUM_O))
        #EEG.segment(N,P,oddchannel)
        #EEG.segment(oddchannel)
       
avg_o = EEG.avg(SUM_O)
print("AVG"+str(avg_o))
       
EEG.classify(avg_e, avg_o)

