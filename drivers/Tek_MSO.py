from matplotlib import style
import pyvisa as visa

class TekScope:

    '''
    A class that uses the vxi11 library to interface a
    Tektronix MSO6 scope.
    Check out https://github.com/python-ivi/python-vxi11
    Last modified: 22/10/2020 by Eugenio Senes
    New modified: June 5th 2026 by Xiaoyu Zhou
    '''

    def __init__(self,address):
        # #USB resource manager of Device
        rm = visa.ResourceManager()
        #    print(rm.list_resources())
        self.device = rm.open_resource(address)
        #    print(device.query("*IDN?"))
        print(self.device.query('*IDN?'))
        self.device.write('HEADer ON')

    # ----- GENERAL SETTINGS
    def release(self):
        self.device.close()

    # ----- FILESYSTEM MANAGEMENT
    def ls_full_directory(self):
        return self.device.query('FIlESystem:DIR?')

    def ls_with_details(self):
        '''
        Returns the detailed file list: for every file you get
        "name; type; size; modification date; modification time"
        '''
        return self.device.query('FIlESystem:LDIR?')

    def get_current_dir(self):
        return self.device.query('FILESystem:CWD?').split(' ')[-1]

    def set_current_dir(self, dirname):
        '''
        This directory must exist. Otherwise no error and not set.
        '''
        return self.device.write('FILESystem:CWD \"'+dirname+'\"')

    def homedir(self):
        return self.device.query('FILESystem:HOMEDir?').split(' ')[-1]

    def rmdir(self, dirname):
        '''
        Removes directory, but it must be empty
        '''
        self.device.write('FILESystem:RMDir \"'+dirname+'\"')

    def mkdir(self, dirname):
        self.device.write('FILESystem:MKDir \"'+dirname+'\"')

    def delete(self, fname):
        self.device.write('FILESystem:DELEte \"'+fname+'\"')

    def rename(self, fname, new_name):
        self.device.write('FILESystem:REName \"'+fname+'\",\"'+new_name+'\"')

    def copy(self, fname, destination):
        self.device.write('FILESystem:COPy \"'+fname+'\",\"'+destination+'\"')

    def unmount_usb(self):
        self.device.write('FILESystem:UNMOUNT:DRIve')

    # ----- ACQUISITION MANAGEMENT
    def acquisition_general_state(self):
        return self.device.query('ACQUIRE?')

    def get_acquisition_mode(self):
        return self.device.query('ACQUIRE:MODe?')

    def set_acquisition_mode(self, state, single_mode=True):
        # acquisition setting, tracewise
        if state in ['SAMple', 'PEAKdetect', 'HIRes', 'AVErage', 'ENVelope']:
            self.device.write('ACQUIRE:MODe '+state)
        else:
            raise ValueError('Unkonwn state')
        #acquisition setting, shotwise
        if single_mode:
            self.device.write('ACQuire:STOPAfter SEQUENCE')
        else:
            self.device.write('ACQuire:STOPAfter RUNSTop')

    ### START/STOP ACQUISITION
    def acquisition_start(self):
        self.device.write('ACQUIRE:STATE 1')

    def acquisition_stop(self):
        self.device.write('ACQUIRE:STATE 0')

    def acquisition_is_running(self):
        return self.device.query('ACQUIRE:STATE?')

    def get_acquisition_number(self):
        '''
        Return the acquisition number from the last RUN command
        '''
        return int(self.device.query('ACQUIRE:NUMAcq?').split(' ')[-1])
    ### AVERAGING MODE --> set mode AVErage
    def get_number_averages(self):
        return int((self.device.query('ACQUIRE:NUMAVg?')).split(' ')[-1])

    def set_number_averages(self, num_avg):
        self.device.write('ACQUIRE:NUMAVg '+str(num_avg))
    ### SEQUENCE MODE --> how many trigger events are acquired
    def get_acquisition_sequence_length(self):
        return int((self.device.query('ACQUIRE:SEQuence:NUMSEQuence?')).split(' ')[-1])

    def set_acquisition_sequence_length(self, num_acq):
        self.device.write('ACQUIRE:SEQuence:NUMSEQuence '+str(num_acq))

    def get_acquisition_sequence_number(self):
        '''
        During a sequence acquisition, returns the current acquisition number
        '''
        return int((self.device.query('ACQUIRE:SEQuence:CURrent?')).split(' ')[-1])
    ### FAST ACQUISITION
    def set_fast_acquisition(self, state):
        if state in ['ON', 'OFF']:
            self.device.write('ACQUIRE:FASTACQ:STATE '+state)
        else:
            raise ValueError('State must be ON or OFF')

    def get_fast_acquitsition(self):
        return (self.device.query('ACQUIRE:FASTACQ:STATE?')).split(' ')[-1]

    # ----- SAVE COMMANDS
    def set_save_destination(self, path):
        self.device.write("SAVEON:FILE:DEST \""+path+'\"')

    def get_save_destination(self):
        return (self.device.query("SAVEON:FILE:DEST?")).split(' ')[-1]

    def set_save_on_trigger(self, state):
        if state in ['ON', 'OFF']:
            self.device.write('SAVEON:TRIGger '+state)
        else:
            raise ValueError('State must be ON or OFF')

    def set_save_waveform(self, state, file_format):
        '''
        Set save waveform on trigger. State = ON/OFF.
        Format = INTERNal / SPREADSheet
        '''
        if state in ['ON', 'OFF']:
            self.device.write('SAVEON:WAVEform '+state)
            if file_format in ['INTERNal','SPREADSheet']:
                self.device.write('SAVEON:WAVEform:FILEFormat '+file_format)
            else:
                raise ValueError('Invalid file format')
        else:
            raise ValueError('State must be ON or OFF')

    def set_save_channel(self, channel):
        if channel in ['CH1', 'CH2', 'CH3', 'CH4', 'ALL']:
            self.device.write('SAVEON:WAVEform:SOURce '+channel)
        else:
            raise ValueError('Invalid channel')
    
    def save_image(self, waveform_path):
        self.device.write(f'SAVE:IMAGE "{waveform_path}"')
    
    ## TODO: the getters ...

    # ----- HORIZONTAL COMMAND GROUP
    def horizontal_general_state(self):
        return self.device.query('HORizontal?')

    def get_horizontal_scale(self):
        return float(self.device.query('HORizontal:SCAle?').split(' ')[-1])

    def set_horizontal_scale(self, h_division):
        '''
        Set horizontal division to the closest possible to the h_division set. 
        Returns the actual division after setting.
        '''
        self.device.write('HORizontal:SCAle '+str(h_division))
        return self.get_horizontal_scale()

    def get_trace_length(self):
        return float(self.device.query('HORizontal:ACQDURATION?').split(' ')[-1])

    def get_horizontal_position(self):
        if bool(int(self.device.query('HORizontal:DELay:MODe?').split(' ')[-1])):
            return float(self.device.query('HORizontal:DELay:TIMe?').split(' ')[-1])
        else:
            return 0.

    def set_horizontal_position(self, hor_delay):
        self.device.write('HORizontal:DELay:MODe ON')
        self.device.write('HORizontal:DELay:TIMe '+str(hor_delay))

    def zero_horizontal_position(self):
        self.device.write('HORizontal:DELay:MODe OFF')

    # ----- VERTICAL COMMAND GROUP
    def get_general_vertical_settings(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return self.device.query(channel+'?')
        else:
            raise ValueError('Invalid channel name')

    def get_channel_bandwidth(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return float(self.device.query(channel+':BANdwidth?').split(' ')[-1])
        else:
            raise ValueError('Invalid channel name')

    def set_channel_bandwidth_limit(self, channel, BW='FULL'):
        '''
        Bandwidth limitation setting for channel <channel>.
        Enter either 'FULL' or the BW in MHz
        '''
        if channel in ['CH1','CH2','CH3','CH4']:
            if BW == 'FULL':
                self.device.write(channel+':BANdwidth FULL')
            else:
                self.device.write(channel+':BANdwidth '+str(BW))
        else:
            raise ValueError('Invalid channel name')

    def channel_is_clipping(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return bool(int(self.device.query(channel+':CLIPping?').split(' ')[-1]))
        else:
            raise ValueError('Invalid channel name')

    def get_channel_coupling(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return self.device.query(channel+':COUPling?').split(' ')[-1]
        else:
            raise ValueError('Invalid channel name')

    def set_channel_coupling(self, channel, coupl):
        if channel in ['CH1','CH2','CH3','CH4'] and coupl in ['AC','DC','DCREJ']:
            self.device.write(channel+':COUPling '+coupl)
        else:
            raise ValueError('Invalid channel name')

    def get_vertical_offset(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return float(self.device.query(channel+':OFFSet?').split(' ')[-1])
        else:
            raise ValueError('Invalid channel name')

    def set_vertical_offset(self, channel, offset):
        if channel in ['CH1','CH2','CH3','CH4']:
            self.device.write(channel+':OFFSet '+str(offset))
        else:
            raise ValueError('Invalid channel name')

    def get_vertical_position(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return float(self.device.query(channel+':POSition?').split(' ')[-1])
        else:
            raise ValueError('Invalid channel name')

    def set_vertical_position(self, channel, offset):
        if channel in ['CH1','CH2','CH3','CH4']:
            self.device.write(channel+':POSition '+str(offset))
        else:
            raise ValueError('Invalid channel name')

    def get_vertical_scale(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return float(self.device.query(channel+':SCAle?').split(' ')[-1])
        else:
            raise ValueError('Invalid channel name')

    def set_vertical_scale(self, channel, scale):
        if channel in ['CH1','CH2','CH3','CH4']:
            self.device.write(channel+':SCAle '+str(scale))
        else:
            raise ValueError('Invalid channel name')

    def get_channel_termination(self, channel):
        if channel in ['CH1','CH2','CH3','CH4']:
            return float(self.device.query(channel+':TERmination?').split(' ')[-1])
        else:
            raise ValueError('Invalid channel name')

    def set_channel_termination(self, channel, term):
        '''
        Set channel termination impedance.
        Possible inputs: '50OHM' or '1MEG'
        '''
        if channel in ['CH1','CH2','CH3','CH4']:
            if term == '50OHM':
                self.device.write(channel+':TERmination 50')
            elif term == '1MEG':
                self.device.write(channel+':TERmination 1000000')
            else:
                raise ValueError('Invalid impedance value')
        else:
            raise ValueError('Invalid channel name')


    def set_channel_label(self, channel, label):
        '''
        Set Channel Waveform Label.
        '''
        if channel in ['CH1','CH2','CH3','CH4','LINE','AUXiliary']:
            self.device.write(channel+':LABel:NAMe '+str(label))

    #----- Measurement Commands -----
    def add_measure_maximum(self):
        '''
        Assumes that no measurements exist
        Adds max as Meas1
        '''
        self.device.write('MEASUrement:ADDMEAS MAXIMUM')
        self.device.write('MEASUrement:MEAS1:SOUrce CH2')

    def add_measure_minimum(self):
        '''
        Assumes that max measurement exists
        Adds min ans Meas2
        '''
        self.device.write('MEASUrement:ADDMEAS MINIMUM')
        self.device.write('MEASUrement:MEAS2:SOUrce CH2')


    def get_measure_max(self):
        '''
        Assumes that Max exists as Meas1
        '''
        return self.device.query('MEASUrement:MEAS1:RESUlts:ALLAcqs:MAXimum?')

    def get_measure_min(self):
        '''
        Assumes that min exists as Meas2
        '''
        return self.device.query('MEASUrement:MEAS2:RESUlts:ALLAcqs:MINimum?')

    def get_measure_type(self,val):
        '''
        parameter val is the measurement number
        '''
        return self.device.query('MEASUrement:MEAS'+val+':TYPe?')

    def set_measure_clear(self):
        self.device.write('CLEAR')

    def set_measure_config(self, idx, channel, type):
        self.device.write(f'MEASU:MEAS{idx}:SOU CH{channel}')
        self.device.write(f'MEASU:MEAS{idx}:TYP {type}')
        self.device.write(f'MEASU:MEAS{idx}:STATE ON')

    def get_measure(self, idx):
        return self.device.query(f'MEASU:MEAS{idx}:VAL?')

    #MEASUrement:ADDMEAS 
    #MEASUrement:MEAS<x>:CCRESUlts:ALLAcqs:MAXimum?
    # ----- TRIGGER COMMAND GROUP
    def get_general_trigger_settings(self):
        return self.device.query('TRIGger?')

    def get_trigger_state(self):
        '''
        Possible outcome: ARMED, AUTO, READY, SAVE, TRIGGER
        '''
        return self.device.query('TRIGger:STATE?').split(' ')[-1]

    def get_trigger_mode(self):
        return self.device.query('TRIGger:A:MODe?').split(' ')[-1]

    def set_trigger_mode(self, mode):
        if mode in ['AUTO','NORMal']:
            self.device.write('TRIGger:A:MODe '+mode)
        else:
            raise ValueError('Invalid trigger mode')

    def get_trigger_holdoff(self):
        mode = self.device.query('TRIGger:A:HOLDoff:BY?').split(' ')[-1]
        if mode == 'RANDOM':
            return mode
        elif mode == 'TIME':
            time = self.device.query('TRIGger:A:HOLDoff:TIMe?').split(' ')[-1]
            return mode+' '+str(time)

    def set_trigger_holdoff(self, mode, t_delay=0):
        '''
        Holdoff mode: random or user specified time.
        '''
        if mode == 'TIMe':
            self.device.write('TRIGger:A:HOLDoff:BY '+mode)
            self.device.write('TRIGger:A:HOLDoff:TIMe '+str(t_delay))
        elif mode == 'RANDom':
            self.device.write('TRIGger:A:HOLDoff:BY '+mode)
        else:
            raise ValueError('Invalid holdoff mode')

    def get_trigger_type(self):
        return self.device.query('TRIGger:A:TYPe?').split(' ')[-1]

    def set_trigger_type(self, type):
        if type in ['EDGE','WIDth','TIMEOut','RUNt','WINdow','LOGIc','SETHold','TRANsition','BUS']:
            self.device.write('TRIGger:A:TYPe '+type)
        else:
            raise ValueError('Invalid trigger type')

    def get_trigger_edge_coupling(self):
        return self.device.query('TRIGger:A:EDGE:COUPling?').split(' ')[-1]

    def set_trigger_edge_coupling(self, coupling):
        if coupling in ['DC','HFRej','LFRej','NOISErej']:
            self.device.write('TRIGger:A:EDGE:COUPling '+coupling)
        else:
            raise ValueError('Invalid trigger coupling')

    def get_trigger_edge_slope(self):
        return self.device.query('TRIGger:A:EDGE:SLOpe?').split(' ')[-1]

    def set_trigger_edge_slope(self, slope):
        if slope in ['RISe','FALL','EITher']:
            self.device.write('TRIGger:A:EDGE:SLOpe '+slope)
        else:
            raise ValueError('Invalid trigger slope')

    def get_trigger_edge_source(self):
        return self.device.query('TRIGger:A:EDGE:SOUrce?').split(' ')[-1]

    def set_trigger_edge_source(self, channel):
        if channel in ['CH1','CH2','CH3','CH4','LINE','AUXiliary']:
            self.device.write('TRIGger:A:EDGE:SOUrce '+channel)
        else:
            raise ValueError('Invalid trigger slope')

    def get_trigger_level(self, channel):
        if channel in ['CH1','CH2','CH3','CH4','LINE','AUXiliary']:
            return self.device.query('TRIGger:A:LEVel:'+channel+'?').split(' ')[-1]
        else:
            raise ValueError('Invalid trigger channel')

    def set_trigger_level(self, channel, level):
        if channel in ['CH1','CH2','CH3','CH4','LINE','AUXiliary']:
            self.device.write('TRIGger:A:LEVel:'+channel+' '+str(level))
        else:
            raise ValueError('Invalid trigger channel')


    # ----- WAVEFORM TRANSFER COMMAND GROUP
    def get_transfer_source(self):
        return self.device.query('DATa:SOUrce?').split(' ')[-1]

    def set_transfer_source(self, channel):
        if channel in self.device.query('DATa:SOUrce:AVAILable?').split(' ')[-1].split(','):
            return self.device.write('DATa:SOUrce '+channel)
        else:
            raise ValueError('Invalid channel selected')

    def get_transfer_encoding(self):
        return self.device.query('DATa:ENCdg?').split(' ')[-1]

    def set_transfer_encoding(self, encoding='ASCII'):
        return self.device.write('DATa:ENCdg '+encoding)

    def get_transfer_n_byte(self):
        return self.device.query('WFMOutpre:BYT_Nr?').split(' ')[-1]

    def set_transfer_n_byte(self, bytes=1):
        return self.device.write('WFMOutpre:BYT_Nr '+str(bytes))

    def get_transfer_start_sample(self):
        return self.device.query('DATa:STARt?').split(' ')[-1]

    def set_transfer_start_sample(self, start_sample=1):
        return self.device.write('DATa:STARt '+str(start_sample))

    def get_transfer_end_sample(self):
        return self.device.query('DATa:STOP?').split(' ')[-1]

    def set_transfer_end_sample(self, stop_sample=1000000):
        return self.device.write('DATa:STOP '+str(stop_sample))

    def transfer_waveform(self, transfer_header=True):
        raw_data = self.device.ask('CURVe?').split(' ')[-1]

        if transfer_header:
            header = self.device.ask('WFMOutpre?')
            return [raw_data, header]
        else:
            return raw_data

    #Cursor controls
    def cursors_horizontal(self,aval=0.0,bval=0.0):
        self.device.write('DISPLAY:WAVEVIEW1:CURSOR:CURSOR1:FUNCTION HBArs')
        self.device.write('DISplay:WAVEView1:CURSor:CURSOR1:HBArs:APOSition '+str(aval))
        self.device.write('DISplay:WAVEView1:CURSor:CURSOR1:HBArs:BPOSition '+str(bval))

    #Display Commands
    def set_display_style(self, style):
        'style = OVErlay | STAcked'
        self.device.write('DIS:WAVEV1:VIEWS '+str(style))

    def set_channel_display(self, channel, display):
        'ON=1, OFF=0'
        self.device.write('SEL:CH'+str(channel)+' '+str(display))   

#############################################################
    # ----- CUSTOM ACQUISTION SETUP
    def setup_single_acquisition(self, shot_number):
        '''
        An acquisition of N shots.
        Then the trigger stops.
        Result --> N traces (saved, if required to)
        '''
        self.acquisition_stop()
        self.set_acquisition_mode('SAMple', single_mode=True)
        self.set_acquisition_sequence_length(shot_number)

    def setup_average_acquisition(self, avg_number):
        '''
        An acquisition of the average of N shots.
        Then the trigger stops.
        Result --> 1 trace (saved, if required to)
        '''
        self.acquisition_stop()
        self.set_acquisition_mode('AVErage', single_mode=True)
        self.set_number_averages(avg_number)

    def setup_save_traces(self, save_folder, channel):
        '''
        Setup to save on each trigger the traces in .xls format.
        Channels: CH1, ..., ALL
        It will try to create the destination folder.
        '''
        self.acquisition_stop()
        self.mkdir(save_folder)
        self.set_save_destination(save_folder)
        self.set_save_on_trigger('ON')
        self.set_save_waveform('ON', 'SPREADSheet')
        self.set_save_channel(channel)

    def setup_edge_trigger(self, channel, level, slope='RISe'):
        '''
        Setup to trigger on a channel, on EDGE mode at a given voltage
        '''
        self.acquisition_stop()
        self.set_trigger_mode('NORMal')
        self.set_trigger_type('EDGE')
        self.set_trigger_edge_coupling('DC')
        self.set_trigger_holdoff('RANDom')
        self.set_trigger_edge_slope(slope)
        self.set_trigger_edge_source(channel)
        self.set_trigger_level(channel, level)

    def setup_waveform_transfer(self, channel, encoding, n_byte, start_sample=1, end_sample=1000000):
        '''
        Setup the waveform transfer over network
        '''
        self.set_transfer_source(channel)
        self.set_transfer_encoding(encoding)
        self.set_transfer_n_byte(n_byte)
        self.set_transfer_start_sample(start_sample)
        self.set_transfer_end_sample(end_sample)