#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Classes."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


import logging
import logging.handlers
import time

import serial

import rsuv3.constants
import rsuv3.util


class RSUV3(object):

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(rsuv3.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(rsuv3.constants.LOG_LEVEL)
        _console_handler.setFormatter(rsuv3.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, serial_port, baud=None, rtscts=None):
        self.baud = baud or rsuv3.constants.SERIAL_BAUD
        self.rtscts = rtscts or rsuv3.constants.RTSCTS
        self.serial_port = serial_port
        self.interface = None

    def __del__(self):
        if self.interface is not None and self.interface.isOpen():
            self.interface.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.interface is not None and self.interface.isOpen():
            self.interface.close()

    def connect(self, timeout=None):
        self.interface = serial.Serial(
            self.serial_port, self.baud, rtscts=self.rtscts)
        self.interface.timeout = timeout or rsuv3.constants.SERIAL_TIMEOUT

    def _read_result(self):
        time.sleep(rsuv3.constants.READ_SLEEP)
        read_data = ''
        while 1:
            read_data = ''.join([
                read_data, self.interface.read(rsuv3.constants.READ_BYTES)])
            waiting_data = self.interface.outWaiting()
            if not waiting_data:
                return read_data.replace('\r', '\n').rstrip().lstrip()

    def _send_command(self, command):
        """
        Sends the given command to the serial interface, followed by CRLF.

        :param command: Command to send.
        :type command: str
        :returns: Serial output result of command.
        :rtype: str
        """
        self._logger.debug('command="%s"', command)
        self.interface.write(command + '\r\n')
        res = self._read_result()
        self._logger.debug('result="%s"', ' '.join(res.split('\n')))
        return res

    def get_firmware(self):
        """
        Gets the current firmware version.

        :returns: Firmware Version.
        :rtype: str
        """
        return self._send_command('FW')

    def get_channel_parameters(self, channel=0):
        """
        Gets channel parameters for the given channel (default channel=0).

        Returns the channel parameters as a dictionary:

            {
                'tx_frequency': '12345',
                'rx_frequency': '12345',
                'tone_frequency': '1234',
                'squelch_mode': 'xxx',
                'power': 'xxx',
                'channel': 'n'
            }

        :param channel: Channel number for which to return parameters.
        :type channel: str
        :returns: Channel Parameters Dictionary.
        :rtype: dict
        """
        params = ('tx_frequency', 'rx_frequency', 'tone_frequency',
            'squelch_mode', 'power')

        cmd = ''.join(['CP', str(channel)])
        res = self._send_command(cmd)

        channel_params = dict(zip(params, res.split()))
        channel_params['channel'] = channel
        return channel_params

    def get_channel_squelch_state(self, channel=0):
        """
        10. CC - Check Squelch State on a Channel
        Command: CC
        Syntax: CCn

        Description: Checks to see if the squelch is open on memory channel n
        Notes: Takes about 50 mS for carrier squelch and 100 mS for
        channels with tone squelch, returns to current operating channel when
        finished.

        Response: 0 - squelch closed; 1 - squelch open
        """
        cmd = ''.join(['CP', str(channel)])
        res = self._send_command(cmd)
        if '0' in res:
            return {'channel': channel, 'squelch_state': 'closed'}
        elif '1' in res:
            return {'channel': channel, 'squelch_state': 'open'}

    def get_cw_beacon_timer(self):
        cmd = ''.join(['BC', '?'])
        return self._send_command(cmd)

    def set_cw_beacon_timer(self, seconds):
        cmd = ''.join(['BC', "%03d" % seconds])
        return self._send_command(cmd)

    def get_beacon_message(self):
        cmd = ''.join(['BM', '?'])
        return self._send_command(cmd)

    def set_beacon_message(self, message):
        cmd = ''.join(['BM', message])
        return self._send_command(cmd)

    def factory_reset(self):
        print self._send_command('FD1')
        return 'Please power-cycle.'

    def set_rx_frequency(self, frequency):
        return self.set_frequency(frequency, 'rx')

    def set_tx_frequency(self, frequency):
        return self.set_frequency(frequency, 'tx')

    def set_frequency(self, frequency, op_arg='both'):
        """
        23. F - Set the RS-UV3 Operating Frequency
        Command: F
        Syntax: Fz nnnnnn or F?

        Description: Sets TX and/or RX frequency (depending on z) to nnnnnn
        kHz Default State: TX - 146.52 MHz; RX 146.52 MHz
        Notes: all digits are required,
        R - Set RX frequency only
        T - Set TX frequency only
        S - Set both TX and RX to same frequency, simplex
        D - Set RX to nnnnnn kHz and TX to nnnnnn - the repeater offset
        U - Set RX to nnnnnn kHz and TX to nnnnnn + the repeater offset
        Repeater offsets: 2M - 600 kHz; 1.25M - 1600 kHz; 70cm -5000 kHz
        Response: F? Reports RX and TX frequencies
        """
        if op_arg == 'both':
            cmd = ''.join(['FS', frequency])
        elif op_arg == 'rx':
            cmd = ''.join(['FR', frequency])
        elif op_arg == 'tx':
            cmd = ''.join(['FT', frequency])
        return self._send_command(cmd)

    def get_frequency(self):
        params = ('tx_frequency', 'rx_frequency')
        res = self._send_command('F?')
        res2 = res.split()
        res3 = dict(zip(params, [res2[1], res2[3]]))
        return res3

    def get_frequency_measurement(self, frequency):
        """
        24. FM - Measure the Signal Level on a Specific Frequency
        Command: FM
        Syntax: FMnnnnnn
        Description: Tunes the RX to nnnnnn kHz measures and reports the
        signal strength then returns to the original frequency
        Default State: N/A
        Notes: all digits required
        Response: Reports the signal strength on the given frequency in dBm
        """
        cmd = ''.join(['FM', frequency])
        return self._send_command(cmd)

    def get_squelch_state(self):
        """
        41. SO - Report the Current State of the Squelch
        Command: SO
        Syntax: SO
        Description: Returns 1 if the squelch is open; 0 if the squelch is
        closed
        Default State: N/A
        Notes: Works with RSSI and CTCSS squelches
        Response: SO: x
        """
        res = self._send_command('SO')
        res2 = res.split()
        if '0' in res2:
            return {'squelch_state': 'closed'}
        elif '1' in res2:
            return {'squelch_state': 'open'}

    def get_squelch_level(self):
        """
        42. SQ - Set the Squelch Level
        Command: SQ
        Syntax: SQn or SQ?
        Description: Sets the level of the RSSI squelch to n
        Default State: 3
        Notes: 0 - 9; 0 = always open, 9 = never open
        Response: SQ? Reports current SQ level
        """
        res = self._send_command('SQ?')
        res2 = res.split()
        return {'squelch_level': res2[1]}

    def set_squelch_level(self, level):
        """
        42. SQ - Set the Squelch Level
        Command: SQ
        Syntax: SQn or SQ?
        Description: Sets the level of the RSSI squelch to n
        Default State: 3
        Notes: 0 - 9; 0 = always open, 9 = never open
        Response: SQ? Reports current SQ level
        """
        cmd = ''.join(['SQ', str(level)])
        res = self._send_command(cmd)
        return self.get_squelch_level()

    def send_dtmf(self, dtmf):
        """
        20. DS - Send a String of DTMF Characters
        Command: DS
        Syntax: DS<text>
        Description: Sends DTMF characters 0,1,2,3,4,5,6,7,8,9,A,B,C,D,* and #
        Default State: N/A
        Notes: Non DTMF characters generate a pause, 28 characters max,
        automatically keys the TX if needed
        Response: N/A
        """
        cmd = ''.join(['DS', dtmf])
        res = self._send_command(cmd)
        return res
