__author__ = 'DVTRF'

from data.parameters import DUT_NAME, RADIO, CHANNEL, ANGLE_NUM, ANGLE_LIST, ATTENUATE_LIST, DURATION
import os
import data.write_datas
import json
import logging
logger = logging.getLogger()

retval = os.getcwd()
result_file = retval + '/Result/iperf3/' + DUT_NAME + '_' + RADIO + '/'


# for Generate test report
class Throught(object):
    def __init__(self, RX, TX):
        self.RX = RX
        self.TX = TX

    def get_tx_throught_simple(self):
        try:
            file_path = result_file + self.TX
            #print('33', file_path)
            f = open(file_path, "r")
            #print('44', f)
        except Exception as err:
            logger.error(err)
        else:
            result = json.load(f)
            try:
                txthrought = float(result['end']['sum_received']['bits_per_second'])/1000000
            #print(txthrought)
            except Exception as err:
                logger.error(err)
            else:
                # data.write_datas.tx_tp_wirte(str(txthrought))
                logger.info("tx_throught is    : {0} ".format(txthrought))
                #data.write_datas.test_time_write(DURA_TIME)
                #print(txthrought)
                f.close()
        return txthrought

    def get_rx_throught_simple(self):
        try:
            file_path = result_file + self.RX
            f = open(file_path, "r")
        except Exception as err:
            logger.error(err)
        else:
            result = json.load(f)
            try:
                rxthrought = float(result['end']['sum_received']['bits_per_second'])/1000000
            except Exception as err:
                logger.error(err)
            else:
                # data.write_datas.rx_tp_write(str(rxthrought))
                logger.info("rx_throught is    : {0} ".format(rxthrought))
                data.write_datas.test_time_write(DURATION)
                #print(rxthrought)
                f.close()
        return rxthrought

if __name__ == "__main__":

    angles = 8
    if angles == 1:
        for i in range(30, 70, 10):
            for angle in [0]:
                RX = []
                TX = []
                rx = " " + str(i) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(i) + "_" + " " + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
    elif angles == 4:
        for atten in range(30, 70, 10):
            for angle in [0, 90, 180, 270]:
                rx = " " + str(atten) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(atten) + "_" + " " + str(angle) + "_Tx.txt"
                RX = []
                TX = []
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
    elif angles == 8:
        for atten in range(30, 70, 10):
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                rx = " " + str(atten) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(atten) + "_" + " " + str(angle) + "_Tx.txt"
                RX = []
                TX = []
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
