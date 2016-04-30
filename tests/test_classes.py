#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for RS-UV3 Classes."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


import random
import unittest
import logging
import logging.handlers

import dummyserial

from . import constants
from .context import rsuv3


class RSUV3Test(unittest.TestCase):  # pylint: disable=R0904
    """Tests for RS-UV3 Class RSUV3."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(rsuv3.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(rsuv3.constants.LOG_LEVEL)
        _console_handler.setFormatter(rsuv3.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    @classmethod
    def random(cls, length=8, alphabet=None):
        """
        Generates a random string for test cases.
        :param length: Length of string to generate.
        :param alphabet: Alphabet to use to create string.
        :type length: int
        :type alphabet: str
        """
        alphabet = alphabet or constants.ALPHANUM
        return ''.join(random.choice(alphabet) for _ in xrange(length))

    def setUp(self):  # pylint: disable=C0103
        self.random_serial_port = self.random()
        self._logger.debug('random_serial_port=%s', self.random_serial_port)
        self.rsuv3 = rsuv3.RSUV3(serial_port=self.random_serial_port)

    def test_get_firmware(self):
        random_firmware = self.random()
        self._logger.debug('random_firmware=%s', random_firmware)
        self.rsuv3.interface = dummyserial.Serial(
            port=self.random_serial_port,
            ds_responses={'FW\r\n': random_firmware}
        )
        self._logger.info('rsuv3 interface=%s', self.rsuv3.interface)

        firmware = self.rsuv3.get_firmware()
        self._logger.debug('firmware=%s', firmware)
        self.assertEqual(firmware, {'firmware_version': random_firmware})

    def test_get_channel_parameters(self):
        random_channel = random.randint(0, 13)
        random_channel_parameters = '\n'.join([
            self.random(6, constants.NUMBERS),
            self.random(6, constants.NUMBERS),
            self.random(5, constants.NUMBERS),
            self.random(1, '01'),
            self.random(1, '01')
        ])
        self._logger.debug('random_channel=%s', random_channel)
        self._logger.debug(
            'random_channel_parameters=%s', random_channel_parameters)

        self.rsuv3.interface = dummyserial.Serial(
            port=self.random_serial_port,
            ds_responses={
                "CP%s\r\n" % random_channel: random_channel_parameters}
        )
        self._logger.info('rsuv3 interface=%s', self.rsuv3.interface)

        channel_parameters = self.rsuv3.get_channel_parameters(random_channel)
        self._logger.debug('channel_parameters=%s', channel_parameters)
        rcp_serialized = rsuv3.util.cp_serializer(
            random_channel_parameters, random_channel)
        self.assertEqual(channel_parameters, rcp_serialized)

    def test_send_dtmf(self):
        dtmf_alpha = constants.NUMBERS + constants.ALPHABET[:3] + '*#'
        rand_len = random.randint(1, 28)
        random_dtmf = self.random(rand_len, dtmf_alpha)
        self._logger.debug('random_dtmf=%s', random_dtmf)

        self.rsuv3.interface = dummyserial.Serial(
            port=self.random_serial_port,
            ds_responses={"DS%s\r\n" % random_dtmf: ''}
        )
        self._logger.info('rsuv3 interface=%s', self.rsuv3.interface)

        dtmf_result = self.rsuv3.send_dtmf(random_dtmf)
        self.assertEqual('', dtmf_result)

    def test_set_squelch_level(self):
        random_squelch_level = self.random(1, constants.NUMBERS)
        self._logger.debug('random_squelch_level=%s', random_squelch_level)

        self.rsuv3.interface = dummyserial.Serial(
            port=self.random_serial_port,
            ds_responses={"SQ%s\r\n" % random_squelch_level: ''}
        )
        self._logger.info('rsuv3 interface=%s', self.rsuv3.interface)

        squelch_level = self.rsuv3.set_squelch_level(random_squelch_level)
        self.assertEqual('', squelch_level)

    def test_get_squelch_level(self):
        random_squelch_level = self.random(1, constants.NUMBERS)
        self._logger.debug('random_squelch_level=%s', random_squelch_level)

        self.rsuv3.interface = dummyserial.Serial(
            port=self.random_serial_port,
            ds_responses={'SQ?\r\n': 'SQ ' + random_squelch_level}
        )
        self._logger.info('rsuv3 interface=%s', self.rsuv3.interface)

        squelch_level = self.rsuv3.get_squelch_level()
        self.assertEqual(
            {'squelch_level': random_squelch_level}, squelch_level)
