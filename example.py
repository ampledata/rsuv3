
import rsuv3

if __name__ == '__main__':
    FRS_13 = '467.6875'

    PORT = '/dev/tty.Repleo-PL2303-0013121A'
    PORT = '/dev/tty.Repleo-PL2303-00003414'
    c = rsuv3.RSUV3(PORT)
    c.connect()
    #print c.get_firmware()
    #print c.set_cw_beacon_timer(0)
    #print c.get_cw_beacon_timer()
    #print c.set_beacon_message('Hello World from W2GMD.')
    #print c.get_beacon_message()
    #print c.set_rx_frequency('146.52')
    #print c.get_frequency()
    #print c.set_tx_frequency('146.52')
    #print c.get_frequency()
    print c.set_frequency(freq_fix(FRS_13))
    print c.get_frequency()
    #print c.get_frequency_measurement('144.39')
    #print c.get_channel_parameters()
    #print c.get_channel_parameters(1)
    #print c.get_channel_squelch_state()
    #print c.get_channel_squelch_state(1)
    #print c.get_frequency()
    #print c.get_squelch_state()
    #print c.get_squelch_level()
    #print c.set_squelch_level(5)
    print c.send_dtmf('ABC')
    #print c.factory_reset()
