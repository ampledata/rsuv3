#!/usr/bin/env python

"""
Example usage for RSUV3 Module.
"""

import rsuv3


if __name__ == '__main__':
    TWO_METER_CALLING = '146.52'
    PORT = '/dev/tty.Repleo-PL2303-00003414'

    conn = rsuv3.RSUV3(PORT)
    conn.connect()

    print(conn.get_firmware())
    print(conn.set_frequency(TWO_METER_CALLING))
    print(conn.get_frequency())
    print(conn.get_squelch_level())
    print(conn.get_squelch_state())
    print(conn.get_channel_squelch_state())
    print(conn.get_channel_parameters())

    #print conn.set_cw_beacon_timer(0)
    #print conn.get_cw_beacon_timer()
    #print conn.set_beacon_message('Hello World from W2GMD.')
    #print conn.get_beacon_message()
    #print conn.set_rx_frequency('146.52')
    #print conn.set_tx_frequency('146.52')
    #print conn.get_frequency_measurement('144.39')
    #print conn.get_channel_parameters(1)
    #print conn.get_channel_squelch_state(1)
    #print conn.set_squelch_level(5)
    #print c.send_dtmf('ABC')
    #print c.factory_reset()

radio = rsuv3.RSUV3('/dev/ttyAMA0')
radio.connect()

frequency = rsuv3.util.fix_frequency(FREQ)

radio.set_frequency(frequency)
radio.set_squelch_level(8)
radio._send_command('TM2')
radio._send_command('TF21810')
radio._send_command('CLW2GMD')  # Set Callsign
radio._send_command('BMW2GMD')  # Set Beacon Message
radio._send_command('BT600')  # Set Beacon Interval

print radio.get_frequency()
print radio._send_command('BM?')  # Report current beacon message
print radio._send_command('BT?')  # Report current beacon time
print radio.get_squelch_level()
print radio.get_squelch_state()
print radio._send_command('ID')  # Send ID
