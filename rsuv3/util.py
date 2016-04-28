#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RS-UV3 Utils."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


def fix_frequency(frequency):
    """
    Fixes the frequency format for RS-UV3.
    """
    return frequency.replace('.', '')


def cp_serializer(cp, channel=0):
    params = (
        'tx_frequency', 'rx_frequency', 'tone_frequency',  'squelch_mode',
        'power'
    )
    channel_params = dict(zip(params, cp.split()))
    channel_params['channel'] = channel
    return channel_params
