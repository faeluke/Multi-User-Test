#----------------------------------------------------------------
#Device Model: Tekronix MSO44
#Version: V2
#Last Modified Date: 2026 June 4
#----------------------------------------------------------------

import pyvisa as visa

class MSO44():

    def __init__(self, desc):
        rm = visa.ResourceManager()

        try:
            print(f"Attempting to oepn: {desc}")
            self.visa = rm.open_resource(desc)
            self.visa.timeout = 5000
            
            ident = self.get_ident()
            print(f"Connected successfully: {ident}")
            
            if not 'TEKTRONIX' in ident:
                print("Warning, attached device", desc, "is not a Tektronix scope")
                print("Device is", ident)
        except visa.VisaIOError as e:
            print(f"Failed to connect to {desc}")
            print(f"Error:{e}")
            raise e
        except Exception as e:
            print(f"Unexpected error:{e}")
            raise e
    
    def release(self):
        """Explicitly close the VISA session"""
        if self.visa:
            self.visa.close()
            print("Scope connection closed.")
    
    def get_ident(self):
        'Return the identity of the device'
        return self.visa.query('*IDN?')    

#Display Commands
    def set_display_style(self, style):
        'style = OVErlay | STAcked'
        self.visa.write('DIS:WAVEV1:VIEWS '+str(style))

    def set_channel_display(self, channel, display):
        'ON=1, OFF=0'
        self.visa.write('SEL:CH'+str(channel)+' '+str(display))

#Channel Commands    
    def set_channel_coupling(self, channel, coupling):
        'Coupling = AC | DC | DCR'
        self.visa.write('CH'+str(channel)+':COUPling '+str(coupling))

    def set_channel_bwlimit(self, channel, bandwidth):
        self.visa.write('CH'+str(channel)+':BANDWIDTH '+str(bandwidth))

    def set_channel_offset(self, channel, offset):
        'set the vertical offset for the specified channel'
        '2mV -> 2e-3'
        self.visa.write('CH'+str(channel)+':OFFS '+str(offset))
    
    def set_channel_position(self, channel, position):
        'set the vertical position for the specified channel'
        self.visa.write('CH'+str(channel)+':POS '+str(position))

    def set_channel_scale(self, channel, scale):
        self.visa.write('CH'+str(channel)+':SCAle '+str(scale))

#Trigger Commands
    def set_trigger_acquire_state(self, state):
        'state = OFF|ON|RUN|STOP'
        self.visa.write(f'ACQuire:STATE {state}')

    def set_trigger_mode(self, trigger_mode):
        'trigger_mode = RUNSTop | SEQuence'
        self.visa.write(f'ACQ:STOPA {trigger_mode}')

    def set_trigger_source(self, channel):
        self.visa.write('TRIGGER:A:EDGE:SOURCE CH'+str(channel))
    
    def set_trigger_position(self, position):
        'set the horizontal tigger position'
        '0=left edge, 100=right edge'
        self.visa.write('HORizontal:POSition '+str(position))

    def set_trigger_level(self, channel, level):
        'level: vertical postion of the triggerd signal'
        self.visa.write('TRIGger:A:LEVel:CH'+str(channel)+' '+str(level))

#Horizontal/Timescale Commands
    def set_horizontal_scale(self, scale):
        'i.e. 20e-9 = 20 ns/division'
        self.visa.write('HORIZONTAL:SCALE '+str(scale))

#System commands
    def create_folder(self, directory_path):
        'directory_path is unquoted string that specifies the directory to create'
        self.visa.write(f'FILESystem:MKDir "{directory_path}"')

    def save_image(self, waveform_path):
        self.visa.write(f'SAVE:IMAGE "{waveform_path}"')

#Measurment Command

#Label Commands   
