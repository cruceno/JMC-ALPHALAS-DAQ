'''
Created on 29 may. 2017

@author: javier
'''

from ftd2xx.ftd2xx import listDevices

class CCDS3600D:
    '''
    classdocs
    '''
    def __init__(self, ft_handler):
        '''
        Constructor
        '''
        #self.ftdconn = ft.FTD2XX(ft_handler)

    def write(self, cmd, value=None):
        ''' Write command to ccd
        '''
        self.ftdconn.write(cmd)

    def read(self, nchars):
        '''Read answer from ccd
        '''
        data = self.ftdconn.read(nchars)
        return data

    def check_ack_or_nack(self):
            # Procesar respuesta
            ack = self.read()
            if ack == b'\x06':
                return True
            if ack == b'\x15':
                return False

    def set_integration_time(self, it=5000):
        '''
        This command sets the integration time in microseconds (μs). The valid range is from 10 μs to 60 s.
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

        if it in range(10, 60000001, 1):
            self.write(b'\xC1', it)

            return self.check_ack_or_nack()

    def set_number_of_frames(self, nf=1):
        '''
        Set Number of Frames (Scans, Readouts) Per Acquisition Command
        This command sets how many frames will be captured in one acquisition. This
        setting applies to onboard data storage mode only. The maximum possible number
        of frames per acquisition is limited by the internal RAM of the device to 4599 (or
        4541 if the user has chosen to include the dummy pixels in the readouts).
        Important note: This setting will be ignored in the advanced data streaming mode
        because the number of frames is not limited in that mode and acquisition will
        continue until it is manually stopped.

        Unit: N/A
        Valid range: 1 – 4599
         (4541 if dummy pixels are included in readouts)
        Default: 1
        Command byte (hex): 0xC2
        Data: 32-bit unsigned integer (4 bytes), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''
        if nf in range(1, 4600, 1):
            self.write(b'\x02', nf)
            return self.check_ack_or_nack()

    def set_ccd_operating_mode(self, cmd=1):
        '''
        Set CCD Operating Mode Command
        This command sets the operating mode of the CCD. The five operating modes
        define the behavior of the device (external or internal synchronization, trigger types,
        etc.). The available operating modes are:
            • 0: Internally synchronized, continuously running, with software capture start
            • 1: Internally synchronized, continuously running, with hardware capture start
            • 2: Internally synchronized, continuously running, with hardware capture enable
            • 3: Single-shot, clean & ready with external hardware trigger
            • 4: Externally synchronized, continuously running, with software capture start

        Unit: N/A
        Valid range: 0 – 4 (please note that the first mode is number 0)
        Default: 0 (Internally synchronized, continuously running, with software capture start)
        Command byte (hex): 0xC3
        Data: 8-bit unsigned integer (1 byte), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)

        '''

        if cmd in range(0, 5, 1):
            self.send(b'\xC3', cmd)
            return self.check_ack_or_nack()

    def set_tirg_out_before_integration_offset(self, ms=0):
        '''
        Set Trig Out Before Integration Offset Command
        This command sets the trig out offset prior to integration start in microseconds (μs).
        This offset can be used to indicate in advance that the integration will begin shortly
        but it is applicable only when the sensor is in shutter mode (i.e. Tint < 3710 μs)
        and applies only to the following four operating modes:
        • Internally synchronized, continuously running, with software capture start
        • Internally synchronized, continuously running, with hardware capture start
        • Internally synchronized, continuously running, with hardware capture enable
        • Single-shot, clean & ready with external hardware trigger
        Important notes:
        In the above operating modes when the sensor is in non-shutter mode this setting
        will be ignored as the integration begins at the start of a new frame and the offset is
        always 0 μs.
        In external synchronization mode this setting is also ignored as the trig out signal has
        a different meaning and indicates when integration has finished (not when it has
        started).
        Unit: microseconds (μs)
        Valid range: 0 μs – 1849 μs
        Default: 0 μs (= no offset)
        Command byte (hex): 0xC4
        Data: 32-bit unsigned integer (4 bytes), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''
        if ms in range(0, 1850, 1):
            self.write(b'\xC4', ms)
            return self.check_ack_or_nack()

    def enable_trigger_output(self, enabled=0):
        '''
        Enable Trigger Output Command (Available since FW A1.10)
        Since firmware A1.10 the trigger output has been disabled by default (set to 0)
        after device initialization and should stay disabled during device configuration. This is
        to prevent glitches from appearing on the trigger output. This feature has been
        implemented in favor of additional protection of external devices connected to the
        trigger output. The user can enable the trigger output before initiating the acquisition
        as required. See also chapter 5.5.
        After having configured all other device parameters, this command can be sent
        with parameter 1 = enabled in order to reenable the trigger output.
        Important note: Please note that this option will be ignored on older devices (FW
        A1.00). Trigger output is always enabled on those devices.

        Unit: N/A
        Valid range: 0 or 1 (0 = disabled, 1 = enabled)
        Default: 0 (= disabled)
        Command byte (hex): 0xE1
        Data: 8-bit unsigned integer (1 byte), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''

        if enabled in range(0, 2, 1):
            self.write(b'\xE1', enabled)
            return self.check_ack_or_nack()

    def set_hardware_dark_correction(self, enabled=0):

        '''
        Set Hardware Dark Correction Command
        This command turns the hardware dark correction of the device on or off. If this
        option is enabled (1) the optically black pixels at the beginning of the sensor will be
        used to automatically compute the average dark level for each frame in real time in
        hardware. This level will be then subtracted from the current signal level for all active
        pixels of that frame.
        Important note: This setting will be ignored if the dummy pixels are set to be included
        in the readouts.
        Unit: N/A
        Valid range: 0 or 1 (0 = disabled, 1 = enabled)
        Default: 0 (= disabled)
        Command byte (hex): 0xC5
        Data: 8-bit unsigned integer (1 byte), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''

        if enabled in range(0, 2, 1):
            self.write(b'\xC5', enabled)
            return self.check_ack_or_nack()

    def include_dummy_pixels_in_readouts(self, enabled=0):

        '''
        Include Dummy Pixels in Readouts Command
        This advanced command is normally not used. We recommend leaving this
        setting disabled. This advanced setting defines if the dummy pixels of the CCD
        sensor will be included in readouts. Because most of these pixels do not contain any
        useful information this setting should be normally left disabled. If disabled, only the
        active pixels of the CCD are included in readouts, which is the default.
        Important note: If this setting is enabled, the Hardware Dark Correction setting will be
        always disabled.
        Unit: N/A
        Valid range: 0 or 1 (0 = disabled, 1 = enabled)
        Default: 0 (= disabled)
        Command byte (hex): 0xC9
        Data: 8-bit unsigned integer (1 byte), MSB first
        Reply from device: ACK (0x06) or NACK (0x15)
        '''

        if enabled in range(0, 2, 1):
            self.write(b'\xC9', enabled)
            return self.check_ack_or_nack()

    def init_adquisition_onboard_data_storage(self):
        '''
        Initiate Acquisition in Onboard Data Storage Mode Command
        (acquisition will auto-stop after capturing the preset number of frames)

        This command initiates an acquisition for the preset number of frames (scans). Up to
        4599 captured frames can be set to be stored in onboard RAM. Acquisition will auto-
        stop after capturing the preset number of frames; no explicit stop command is
        required.

        Important notes: After acquisition of the specified number of frames is
        complete, the device immediately starts sending all captured data to the PC.
        This data must be then fetched by the host PC. Before the acquired data has
        been fetched, the device cannot process further commands. Any further
        commands will be accepted after data has been fetched which may take a few
        seconds because of the large internal storage of the device. E.g. turning the
        trigger output off will take effect with some delay after the actual acquisition
        has finished and the trigger output will still be active during this time. Just keep
        this in mind.

        Command byte (hex): 0xC6
        Data: N/A
        Reply from device: When acquisition of the specified number of frames has finished,
        the device will return all pixel data values from all captured frames. Each frame
        consists of 3648 pixel data values (or 3694 pixel data values if the dummy pixels are
        included). Each data value is 16 bits (2 bytes), MSB first.
        '''

        self.write(b'x\C6')

    def initiate_adquisition_in_data_streaming_until_stop(self):
        '''
        Initiate Acquisition in Data Streaming Mode and Stream Data Until Manually
        Stopped Command (does not use the preset number of frames)

        This command initiates an acquisition in data streaming mode. In this mode the
        device will immediately stream any captured data to the host PC. There is no frame
        limit. The only limit is the storage device used (please also observe the maximum file
        size allowed by the underlying file system used on your storage device). In this
        advanced mode the configured number of frames (scans) per acquisition is
        completely ignored. Instead, the acquisition of triggered scans will continue until it is
        manually stopped by sending the Stop Acquisition and Data Streaming command
        (described below). After receiving the stop command, the device will capture one
        more frame and then stop acquisition. During streaming, the onboard RAM is used
        as a big FIFO frame buffer and prevents data overflow during capture.

        During acquisition, acquired data will be continuously streamed to the PC and each
        scan must be fetched in time. The device features advanced buffering technology
        allowing the PC to fetch the data without buffer overflows. Nevertheless, the user
        must make sure that data is fetched as soon as possible and written to disk.
        Because in streaming mode the constant data rate is very high, it is not
        recommended to attempt to view the streaming data in real time. Instead, write the
        data to disk and view it later.

        Programming logic tips: As described, during streaming one should periodically fetch
        captured frames. As soon as acquisition has been stopped by calling the Stop
        Acquisition and Data Streaming command, it is not sure if there are more scans to
        arrive that have to be fetched. If there are frames left in the buffer after acquisition is
        stopped, they will be still streamed to the PC. Therefore, the incoming device buffer
        should be checked for pending data even after acquisition has been stopped; if there
        is such data, it should be fetched. If there is no data in the buffer for a longer time,
        the last streaming data has been already fetched and the acquisition is complete.
        The FIFO RAM buffer is very large and should be able to buffer data without
        overflowing if the data is regularly fetched by the host PC. Nevertheless, if the buffer
        should overflow for some reason, this will be indicated by the red error LED on the
        device. In this case, streaming will be aborted. Please disconnect and reconnect the
        device from USB in order to reset it in case of this error.
        Programming in data streaming mode is recommended for advanced users only. If
        you are using LabVIEW, please look at the included data streaming applications for
        more information.

        Command byte (hex): 0xC7
        Data: N/A
        Reply from device: Acquired pixel data values will be immediately and continuously
        streamed to the host PC during acquisition. After acquisition has been stopped, if
        there is still data in the frame buffer, it will be also streamed to the PC. Each frame
        consists of 3648 pixel data values (or 3694 pixel data values if the dummy pixels are
        included). Each data value is 16 bits (2 bytes), MSB first.
        '''

        self.write(b'x\C7')

    def stop_adquisition_data_streaming(self):

        '''
        Stop Acquisition and Data Streaming Command
        This command stops the current acquisition and streaming in data streaming mode.
        In this advanced mode the configured number of scans per acquisition is completely
        ignored. Instead, the acquisition of triggered scans will continue until it is manually
        stopped by sending this command.

        As soon as we have stopped acquisition by sending this command, we are not sure if
        there are more scans to arrive that have to be fetched. Therefore, we should
        continue to check for pending data in the incoming device buffer. If there is more
        data to be fetched, we can then fetch the scans. If there is no data in the buffer for a
        longer time, the last streaming data has been already fetched and the acquisition is
        complete.

        Programming in data streaming mode is recommended for advanced users only. If
        you use LabVIEW, please look at the included data streaming applications for more
        information.

        Command byte (hex): 0xC8
        Data: N/A
        Reply from device: The device will stream the last data left in the buffer.
        '''

        self.write(b'x\C8')

