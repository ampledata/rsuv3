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
