#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Classes."""

from __future__ import print_function

import logging
import time

import serial

import rsuv3

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


class RSUV3(object):

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(rsuv3.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(rsuv3.LOG_LEVEL)
        _console_handler.setFormatter(rsuv3.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, serial_port, baud=None, rtscts=None):
        self.baud = baud or rsuv3.SERIAL_BAUD
        self.rtscts = rtscts or rsuv3.RTSCTS
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
        self.interface.timeout = timeout or rsuv3.SERIAL_TIMEOUT

    def _read_result(self):
        """Reads data from RS-UV3 serial interface."""
        time.sleep(rsuv3.READ_SLEEP)
        read_data = ''
        while 1:
            read_data = ''.join([
                read_data, self.interface.read(rsuv3.READ_BYTES)])
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

    def get_status(self):
        """Gets the current status of the RS-UV3."""
        self.get_firmware_version()
        self.get_squelch_level()
        self.get_frequency()
        self.get_tone_frequency()
        self.get_voltage()
        self.get_volume_level()
        self.get_ctcss_mode()
        self.get_squelch_state()
        self.get_noise_level()
        self.get_callsign()
        return {
            'firmware_version': self.firmware_version,
            'squelch_level': self.squelch_level,
            'rx_frequency': self.rx_frequency,
            'tx_frequency': self.tx_frequency,
            'tone_frequency': self.tone_frequency,
            'voltage': self.voltage,
            'volume_level': self.volume_level,
            'ctcss_mode': self.ctcss_mode,
            'squelch_state': self.squelch_state,
            'noise_level': self.noise_level,
            'callsign': self.callsign
        }

    def get_firmware_version(self):
        """Gets Firmware Version."""
        res = self._send_command('FW')
        self.firmware_version = res.split()[-1]
        return self.firmware_version

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
        print(self._send_command('FD1'))
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
        freq = '{:0<6}'.format(rsuv3.fix_frequency(frequency))

        if op_arg == 'both':
            cmd = ''.join(['FS', freq])
        elif op_arg == 'rx':
            cmd = ''.join(['FR', freq])
        elif op_arg == 'tx':
            cmd = ''.join(['FT', freq])

        return self._send_command(cmd)

    def get_frequency(self):
        """Gets the current frequency from the RS-UV3."""
        params = ('tx_frequency', 'rx_frequency')
        res = self._send_command('F?')
        res2 = res.split()
        res3 = dict(zip(params, [res2[1], res2[3]]))
        self.rx_frequency = float(
            '{:3.4f}'.format(float(res3['rx_frequency']) / 1000))
        self.tx_frequency = float(
            '{:3.4f}'.format(float(res3['tx_frequency']) / 1000))
        return res3

    def get_frequency_measurement(self, frequency):
        """
        Measure the Signal Level on a Specific Frequency

        Syntax: FMnnnnnn

        Description: Tunes the RX to nnnnnn kHz measures and reports the
        signal strength then returns to the original frequency

        Response: Reports the signal strength on the given frequency in dBm
        """
        freq = '{:0<6}'.format(rsuv3.fix_frequency(frequency))
        cmd = ''.join(['FM', freq])
        return self._send_command(cmd)

    def get_squelch_state(self):
        """
        Gets the current Squelch State.

        Notes: Works with RSSI and CTCSS squelches.
        """
        res = self._send_command('SO')
        res2 = res.split()
        if '0' in res2:
            self.squelch_state = 'closed'
        elif '1' in res2:
            self.squelch_state = 'open'
        return self.squelch_state

    def get_squelch_level(self):
        """Gets RSSI Squelch Level."""
        res = self._send_command('SQ?')
        self.squelch_level = int(res.split()[-1])
        return self.squelch_level

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

        DTMF characters are in the set of: [0-9, A-D, *, #]

        Notes:
            * Non-DTMF characters generate a pause
            * 28 characters MAX
            * Will automatically key the TX if needed
        """
        cmd = ''.join(['DS', dtmf])
        res = self._send_command(cmd)
        return res

    def set_tone_frequency(self, tone_frequency=None):
        """Sets CTCSS tone frequency."""
        tone_frequency = tone_frequency or rsuv3.DEFAULT_TONE_FREQUENCY
        cmd = ''.join(
            ['TF', '{:0<5}'.format(rsuv3.fix_frequency(tone_frequency))])
        res = self._send_command(cmd)
        return res

    def get_tone_frequency(self):
        """Gets CTCSS tone frequency."""
        res = self._send_command('TF?')
        res2 = res.split()[-1]
        self.tone_frequency = float('{:3.2f}'.format(float(res2) / 100))
        return self.tone_frequency

    def set_volume_level(self, level=None):
        """
        Sets volume level from 0 to 39 in 1 dB steps.

        Note: DTMF decode works best with vloume 10

        :param level: Volume level.
        :type level: int
        """
        level = level or rsuv3.DEFAULT_VOLUME
        cmd = ''.join(['VU', '{:0>2}'.format(level)])
        res = self._send_command(cmd)
        return res

    def get_volume_level(self):
        """Gets Volume Level."""
        self.volume_level = int(self._send_command('VU?').split()[-1])
        return self.volume_level

    def start_transmitter(self, duration=1):
        """
        Turns the transmitter ON for duration.

        Note:
            * Duration of 0 turns OFF the transmitter.
            * Duration of n turns ON the transmitter for n-Minutes.
        """
        cmd = ''.join(['TX', duration])
        res = self._send_command(cmd)
        return res

    def stop_transmitter(self):
        """Turns the transmitter OFF."""
        cmd = ''.join(['TX', 0])
        res = self._send_command(cmd)
        return res

    def get_voltage(self):
        """
        Returns operating/battery voltage.

        Ranges from 8.5 V with external power, 6.5 V to 8.5 V on battery.
        """
        res = self._send_command('VT')
        res2 = res.split('VT:')[-1].lstrip().replace('V', '')
        self.voltage = float(res2)
        return self.voltage

    def set_ctcss_mode(self, mode=None):
        """
        Sets CTCSS Mode.

        Where 'mode' is one of:
            * 0 = CTCSS Tone Off
            * 1 = TX CTCSS Tone
            * 2 = TX & RX CTCSS Tone (a.k.a Tone Squelch)
        """
        cmd = ''.join(['TM', mode])
        res = self._send_command(cmd)
        return res

    def get_ctcss_mode(self):
        """Gets CTCSS Mode."""
        self.ctcss_mode = int(self._send_command('TM?').split()[-1])
        return self.ctcss_mode

    def get_noise_level(self):
        """Gets RX Noise Level."""
        res = self._send_command('SN')
        self.noise_level = int(res.split()[-1].lstrip())
        return self.noise_level

    def set_callsign(self, callsign):
        """Sets Callsign."""
        cmd = ''.join(['CL', callsign])
        res = self._send_command(cmd)
        return res

    def get_callsign(self):
        """Gets Callsign."""
        res = self._send_command('CL?')
        self.callsign = res.split('CL:')[-1].lstrip()
        return self.callsign

    def identify(self):
        """
        Sends the Callsign in Audio CW, automatically keys the TX if needed.
        """
        res = self._send_command('ID')
        return res
