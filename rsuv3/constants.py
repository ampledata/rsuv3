#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Constants."""

import os
import logging

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


if bool(os.environ.get('DEBUG')):
    LOG_LEVEL = logging.DEBUG
    logging.debug('Debugging Enabled via DEBUG Environment Variable.')
else:
    LOG_LEVEL = logging.INFO

LOG_FORMAT = logging.Formatter(
    '%(asctime)s rsuv3 %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
    ' - %(message)s')

SERIAL_BAUD = 19200
SERIAL_TIMEOUT = 0.01
READ_BYTES = 1000
RTSCTS = 0
READ_SLEEP = 1

DEFAULT_VOLUME = 10
DEFAULT_TONE_FREQUENCY = 131.8

COMMANDS = {
    'callsign': 'CL',

    'audio_lowpass_filter': 'AF',
    'audio_highpass_filter': 'HP',
    'deemphasis_preemphasis': 'DP',

    'arduino_din': 'AI',
    'arduino_dout': 'AO',

    'serial1_baud': 'B1',
    'serial2_baud': 'B2',

    'check_squelch': 'CC',
    'channel_parameters': 'CP',

    'beacon_message': 'BM',
    'rf_cw_beacon_timer': 'BC',
    'audio_cw_beacon_timer': 'BT',

    'cw_speed': 'CS',
    'cw_audio_text': 'CT',
    'cw_rf_text': 'CW',
    'cw_audio_tone_frequency': 'CF',
    'cw_id_timer': 'IT',

    'dtmf_duration': 'DD',
    'dtmf_detection': 'DR',
    'dtmf_string': 'DS',

    'ex_pin': 'EX',
    'factory_defaults': 'FD1',
    'frequency': 'F',
    'frequency_measurement': 'FM',
    'firmware': 'FW',
    'mic_gain': 'GM',
    'dtmf_cw_tx_gain': 'GT',
    'hangtime': 'HT',
    'identify': 'ID',
    'st_led_func': 'LD',
    'multichannel_beacon': 'MC',
    'powerdown': 'PD',
    'tx_power': 'PW',
    'recall_channel': 'RC',
    'read_register': 'RR',
    'set_register': 'RS',
    'sidetone': 'SD',
    'signal_noise': 'SN',
    'squelch': 'SQ',
    'signal_strength': 'SS',
    'store': 'ST',
    'to_message': 'TG',
    'timeout': 'TO',
    'receiver_temperature': 'TP',
    'transmit': 'TX',
}
