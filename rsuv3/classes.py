#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Classes."""

import logging
import logging.handlers
import time

import serial

import rsuv3.constants
import rsuv3.util

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


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
        """
        Initializes serial connection to the RS-UV3.

        :param timeout: Timeout in seconds.
        :type timeout: int
        """
        self.interface = serial.Serial(
            self.serial_port, self.baud, rtscts=self.rtscts)
        self.interface.timeout = timeout or rsuv3.constants.SERIAL_TIMEOUT

    def _read_result(self):
        """Reads data from RS-UV3 serial interface."""
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

        Returns the result of the command.

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
        Gets & Returns the current firmware version as a dictionary:

            {
                'firmware_version': 'xxx'
            }

        :returns: Firmware Version as a dictionary.
        :rtype: dict
        """
        res = self._send_command('FW')
        return {'firmware_version': res}

    def get_channel_parameters(self, channel=0):
        """
        Gets channel parameters for the given channel (default channel=0).

        Returns the channel parameters as a dictionary:

            {
                'tx_frequency': '123450',
                'rx_frequency': '123450',
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
        cmd = ''.join(['CP', str(channel)])
        res = self._send_command(cmd)
        return rsuv3.util.cp_serializer(res, channel)

    def get_channel_squelch_state(self, channel=0):
        """
        Gets the Squelch State for the given channel (default channel=0).

        Returns 'Squelch State' as either "open" or "closed" in a dictionary:

            {
                'squelch_state': 'open',  # or 'closed'
                'channel': 'n'
            }

        Notes: Takes about 50 mS for carrier squelch and 100 mS for channels
        with tone squelch.

        :param channel: Channel number for which to return parameters.
        :type channel: str
        :returns: Squelch State as a dictionary.
        :rtype: dict
        """
        cmd = ''.join(['CP', str(channel)])
        res = self._send_command(cmd)
        # TODO: Could probably use better string checking here (vs. '0' in x).
        if '0' in res:
            return {'channel': channel, 'squelch_state': 'closed'}
        elif '1' in res:
            return {'channel': channel, 'squelch_state': 'open'}

    def factory_reset(self):
        """Resets the RS-UV3 to factory settings. Requires a power-cycle."""
        print self._send_command('FD1')
        return 'Please power-cycle the RS-UV3.'

    def set_rx_frequency(self, frequency):
        """Wrapper for set_frequency that sets only the RX frequency."""
        return self.set_frequency(frequency, 'rx')

    def set_tx_frequency(self, frequency):
        """Wrapper for set_frequency that sets only the TX frequency."""
        return self.set_frequency(frequency, 'tx')

    # TODO: Add additional supported params for repeater offsets:
    #  D - Set RX to nnnnnn kHz and TX to nnnnnn - the repeater offset
    #  U - Set RX to nnnnnn kHz and TX to nnnnnn + the repeater offset
    #  Repeater offsets: 2M - 600 kHz; 1.25M - 1600 kHz; 70cm -5000 kHz
    def set_frequency(self, frequency, op_arg='both'):
        """
        Sets the RS-UV3 to the specified Operating Frequency(ies).

        Frequency is in 6 numerical digit format in kHz with no punctuation,
        that is: 146.520 MHz is 146520 kHz.

        See fix_frequency() in utils.

        Can set either TX ('tx'), RX ('rx') or Both [simplex] ('both')
        frequencies (default=both).

        :param frequency: Frequency to set.
        :param op_arg: TX Frequency, RX Frequency or Both Frequencies.
        """
        if op_arg == 'both':
            cmd = ''.join(['FS', frequency])
        elif op_arg == 'rx':
            cmd = ''.join(['FR', frequency])
        elif op_arg == 'tx':
            cmd = ''.join(['FT', frequency])
        return self._send_command(cmd)

    def get_frequency(self):
        """Gets the current frequency from the RS-UV3."""
        params = ('tx_frequency', 'rx_frequency')
        res = self._send_command('F?')
        res2 = res.split()
        res3 = dict(zip(params, [res2[1], res2[3]]))
        return res3

    def get_frequency_measurement(self, frequency):
        """
        Measure the Signal Level on a Specific Frequency

        Syntax: FMnnnnnn

        Description: Tunes the RX to nnnnnn kHz measures and reports the
        signal strength then returns to the original frequency

        Response: Reports the signal strength on the given frequency in dBm
        """
        cmd = ''.join(['FM', frequency])
        return self._send_command(cmd)

    def get_squelch_state(self):
        """
        Gets the current Squelch State.

        Notes: Works with RSSI and CTCSS squelches.
        """
        res = self._send_command('SO')
        res2 = res.split()
        if '0' in res2:
            return {'squelch_state': 'closed'}
        elif '1' in res2:
            return {'squelch_state': 'open'}

    def get_squelch_level(self):
        """
        Gets & Returns the current RSSI Squelch Level as a dictionary:

            {
                'squelch_level': n
            }

        :returns: Squelch Level as a dictionary.
        :rtype: dcit
        """
        res = self._send_command('SQ?')
        # FIXME: Why did I put a split() call here?
        res2 = res.split()
        return {'squelch_level': res2[1]}

    def set_squelch_level(self, level):
        """
        Sets the RSSI Squelch Level to specified level.

        Squelch Level range is 0 to 9, with 0 being 'always open' and '9'
        being 'never open'.
        """
        cmd = ''.join(['SQ', str(level)])
        return self._send_command(cmd)

    def send_dtmf(self, dtmf):
        """
        Immediately transmits a string of DTMF Characters.

        DTMF characters are in the set of:
            [0-9,A-D,*,#]

        Notes: Non DTMF characters generate a pause, 28 characters max,
        automatically keys the TX if needed
        """
        cmd = ''.join(['DS', dtmf])
        res = self._send_command(cmd)
        return res
