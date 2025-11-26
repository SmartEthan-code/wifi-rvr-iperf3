# -*- coding:utf-8 -*-

__author__ = 'DVTRF'

import os
import logging
from time import sleep
from data.parameters import DUT_NAME, DUT_TYPE, RADIO
retval = os.getcwd()
result_file = retval + '/Result/Data/' + DUT_NAME +  '_' + RADIO + '/'
ixchraiot_file = retval + '/Result/IxChariotOD/' + DUT_NAME + '_' + RADIO + '/'

logger = logging.getLogger()


def dutinfo_write(dutinfo):
    with open(result_file + "dutinfo.txt", "a") as ch:
        ch.truncate()
        ch.write(dutinfo)
        ch.write("\n")

def channel_write(channel):
    with open(result_file + "channel.txt", "a") as ch:
        ch.truncate()
        ch.write(channel)
        ch.write("\n")


def atten_write(attention):
    with open(result_file + "attention.txt", "a") as att:
        att.truncate()
        att.write(attention)
        att.write("\n")


def angle_write(angle):
    with open(result_file + "angle.txt", "a") as agl:
        agl.truncate()
        agl.write(str(angle))
        agl.write("\n")


def ap_rssi_write(aprssi):
    with open(result_file + "ap_rssi.txt", "a") as ap_rssi:
        ap_rssi.truncate()
        ap_rssi.write(aprssi)
        ap_rssi.write("\n")


def sta_rssi_write(starssi):
    with open(result_file + "sta_rssi.txt", "a") as sta_rssi:
        sta_rssi.write(starssi)
        sta_rssi.write("\n")


def tx_linkrate_write(txlinkrate):
    with open(result_file + "tx_linkrate.txt", "a") as tx_linkrate:
        tx_linkrate.write(txlinkrate)
        tx_linkrate.write("\n")


def rx_linkrate_write(rxlinkrate):
    with open(result_file + "rx_linkrate.txt", "a") as rx_linkrate:
        rx_linkrate.write(rxlinkrate)
        rx_linkrate.write("\n")


def tx_tp_wirte(txthrought):
    with open(result_file + "tx_tp.txt", "a") as tx_tp:
        #print(tx_tp)
        tx_tp.write(txthrought)
        tx_tp.write("\n")


def rx_tp_write(rxthrought):
    with open(result_file + "rx_tp.txt", "a") as rx_tp:
        rx_tp.write(rxthrought)
        rx_tp.write("\n")


def test_time_write(time):
    sleep(2)
    with open(result_file + "test_time.txt", "a") as test_time:
        sleep(1)
        test_time.write(str(time))
        test_time.write("\n")


def mcs_txrate_write(txrate):
    sleep(1)
    with open(result_file + "mcs_txrate.txt", "a") as mcs_txrate:
        sleep(1)
        mcs_txrate.write(str(txrate))
        mcs_txrate.write("\n")


def mcs_rxrate_write(rxrate):
    sleep(1)
    with open(result_file + "mcs_rxrate.txt", "a") as mcs_rxrate:
        sleep(1)
        mcs_rxrate.write(str(rxrate))
        mcs_rxrate.write("\n")


def nss_txrate_write(txrate):
    sleep(1)
    with open(result_file + "nss_txrate.txt", "a") as nss_txrate:
        sleep(1)
        nss_txrate.write(str(txrate))
        nss_txrate.write("\n")


def nss_rxrate_write(rxrate):
    sleep(1)
    with open(result_file + "nss_rxrate.txt", "a") as nss_rxrate:
        sleep(1)
        nss_rxrate.write(str(rxrate))
        nss_rxrate.write("\n")


def bw_txrate_write(txrate):
    sleep(1)
    with open(result_file + "bw_txrate.txt", "a") as bw_txrate:
        sleep(1)
        bw_txrate.write(str(txrate))
        bw_txrate.write("\n")


def bw_rxrate_write(rxrate):
    sleep(1)
    with open(result_file + "bw_rxrate.txt", "a") as bw_rxrate:
        sleep(1)
        bw_rxrate.write(str(rxrate))
        bw_rxrate.write("\n")


def rssi_txant_write(txrssi):
    sleep(1)
    with open(result_file + "rssi_txant.txt", "a") as rssi_txant:
        sleep(1)
        rssi_txant.write(str(txrssi))
        rssi_txant.write("\n")


def power_txant_write(txpower):
    sleep(1)
    with open(result_file + "power_txant.txt", "a") as power_txant:
        sleep(1)
        power_txant.write(str(txpower))
        power_txant.write("\n")


def rssi_rxant_write(rxrssi):
    sleep(1)
    with open(result_file + "rssi_rxant.txt", "a") as rssi_rxant:
        sleep(1)
        rssi_rxant.write(str(rxrssi))
        rssi_rxant.write("\n")


def power_rxant_write(rxpower):
    sleep(1)
    with open(result_file + "power_rxant.txt", "a") as power_rxant:
        sleep(1)
        power_rxant.write(str(rxpower))
        power_rxant.write("\n")


if __name__ == '__main__':
    for i in range(58, 87, 2):
        atten_write(str(i))
