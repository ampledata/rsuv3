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
