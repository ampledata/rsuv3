#!/usr/bin/env python
# -*- coding: utf-8 -*-

# RSUV3 Python Library.

"""
RSUV3 Python Library.
~~~~

:author: Greg Albrecht W2GMD <oss@undef.net>
:copyright: Copyright 2017 Greg Albrecht
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/rsuv3>
"""

from .constants import (LOG_FORMAT, LOG_LEVEL, SERIAL_TIMEOUT, RTSCTS,  # NOQA
                        SERIAL_BAUD, READ_BYTES, READ_SLEEP, DEFAULT_VOLUME,
                        DEFAULT_TONE_FREQUENCY)

from .util import fix_frequency  # NOQA

from .classes import RSUV3  # NOQA

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__copyright__ = 'Copyright 2017 Greg Albrecht'
__license__ = 'Apache License, Version 2.0'
