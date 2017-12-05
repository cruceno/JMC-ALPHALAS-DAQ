'''
Created on 29 may. 2017

@author: javier
'''
from ftd2xx import *


class ccdCommand(object):
    '''
    classdocs
    '''
    def __init__(self, cmdByte, cmdData, ):
        '''
        Parameters:
        -----------
        byte: CCD command byte
        data: Data to send
        '''
        cmdByte = cmdByte
        cmdName = cmdData


class ftdConnector(FTD2XX):
    '''
    classdoc
    '''
    def __init__(self):
        super(ftdConnector, self).__init__()


class CCDS3600D(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        ftdconn = FTD2XX()

    def write(self):
        ''' Write command to ccd
        '''
        self.
    def read(self):
        '''Read answer from ccd
        '''
    def set_integration_time(self, it=5000):
        '''This command sets the integration time in microseconds (μs). The valid range is from 10 μs to 60 s.
        For integration times from 10 μs to 3709 μs the sensor operates in shutter mode. For
        integration times equal to or above 3710 μs the sensor operates in non-shutter
        mode.
        Important notes:
        In single shot mode the integration time should be set to ≤ 500 μs.
        The integration time setting will be ignored in external synchronization trigger mode
        because the external trigger period will define the integration time in that mode.

        Unit: microseconds (μs)
        Valid range: 10 μs – 60 000 000 μs
        Default: 5000 μs = 5 ms
        Command byte (hex): 0xC1
        Data: 32-bit unsigned integer (4 bytes), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''

        self.send(b'\xC1', it)

        ack = self.read()

        if ack == b'\x06':
            return True
        if ack == b'\x15':
            return False



