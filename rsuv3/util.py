#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Utils."""

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'


def fix_frequency(frequency):
    """
    Fixes the frequency format for RS-UV3.
    """
    return str(frequency).replace('.', '')


def cp_serializer(raw_cp, channel='0'):
    """
    Serializses RS-UV3 Channel Parameters into a Dictionary.

    :param channel: Channel Parameters.
    :type channe: str
    :returns: Dictionary of Channel Parameters.
    :rtype: dict
    """
    params = (
        'tx_frequency', 'rx_frequency', 'tone_frequency', 'squelch_mode',
        'power'
    )
    channel_params = dict(zip(params, raw_cp.split()))
    channel_params['channel'] = channel
    return channel_params
