import sys
sys.path.insert(0, "../../TOMBAK/base-folder/build/lib/aerodiode/")
from tombak import Tombak
from aerodiode import Aerodiode


class pp():
    def __init__(self):
        """ init funtion to initialize tombak in divider mode
        
        Keyword arguments:
        none -- none so far
        """
        # fixed serial port
        self.tombak = Tombak('/dev/serial/by-id/usb-FTDI_TTL-232R-3V3-AJ_FTCAVMZN-if00-port0')
        # set tombak to divder mode needs to be set
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE, self.tombak.DIVIDER)
        # set tombak to fixed pulse width 5 ns
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_OUT_WIDTH, 5)
        # set to direct (not dsaisy chain) mode
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_PULSE_IN_SRC, self.tombak.DIRECT)
        # set trigger to internal since we dont use it
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_TRIGGER_SRC, self.tombak.INT)
        # set monitor out on to see pulse in osci
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_SYNC_OUT_1_SRC, self.tombak.PULSE_OUT)#ok
        # initialize divder
        self.divider = 10
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, self.divider)
        #don't forget to apply settings
        self.tombak.apply_all()
        
    def get_inputFreqency(self):
        """ get input frequency (eg laser)
        
        Keyword arguments:
        returns -- frequency in Hz
        """
        return self.tombak.measure_pulse_in_frequency()
    
    def get_outputFreqency(self):
        """ get output frequency
        
        Keyword arguments:
        returns -- frequency in Hz
        """
        return self.tombak.measure_pulse_in_frequency()/self.divider
    
    def set_outputDivider(self, div):
        """ set output frequency divider
        
        Keyword arguments:
        div -- divider
        returns -- divided frequency in Hz
        """
        self.divider = div
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, div)
        self.tombak.apply_all()
        return self.get_outputFreqency()
    
        
        """ set output pulse width in ns
        
        Keyword arguments:
        w -- pulse length in ns
        """
        self.tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, w)
        self.tombak.apply_all()
        
    def close(self):
        """ switches off tombak by setting pulse length to long
        """
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_OUT_WIDTH, 2E64-1)
        self.tombak.apply_all()
        

    def tenmhz(self):
        """ set output frequency 10MHz
        divide by 8 I tried to get div=self.tombak.measure_pulse_in_frequency()/10000000 but
        only works with nearest interger for division
        returns -- 10 MHz aproximately
        """
        div=8
        #div=self.tombak.measure_pulse_in_frequency()/10000000
        #print(div)
        self.divider = div
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV,div)
        self.tombak.apply_all()
        return self.get_outputFreqency()
        