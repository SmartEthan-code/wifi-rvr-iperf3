__author__ = 'DVTRF'

import os
from data.parameters import DUT_NAME, RADIO
import logging
logger = logging.getLogger()

Dutinfo = []
Att_rep = []
Channel = []
Angle = []
Tx_Throught = []
Rx_Throught = []
Sta_Rssi = []
Ap_Rssi = []
Tx_Rate = []
Rx_Rate = []
Dura_Time = []
MCS_Tx_Rate = []
MCS_Rx_Rate = []
NSS_Tx_Rate = []
NSS_Rx_Rate = []
BW_Tx_Rate = []
BW_Rx_Rate = []
TX_RSSI_ANT = []
TX_POWER_ANT = []
RX_RSSI_ANT = []
RX_POWER_ANT = []

"""
此部分是生成报告时用到的，主要功能是将.txt文件里的数据转换成相应的list，
生成报告时，直接从这些list当中取数据写入excel文件。

在生成报告之前，要首先执行此部分脚本
"""
retval = os.getcwd()
result_file = retval + '/Result/Data/' + DUT_NAME + '_' + RADIO + '/'


class Reportdata_Get(object):
    def __init__(self):
        pass

    @staticmethod
    def Dutinfo_get():
        L = []
        dut_path = result_file + "dutinfo.txt"
        try:
            dut = open(dut_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for info in dut:
                L.append(info)
            for i in range(len(L)):
                Dutinfo.append(L[i].strip())
            return Dutinfo
        except Exception as err:
            logger.info(err)
        finally:
            dut.close()

    @staticmethod
    def Ch_get():
        L = []
        ch_path = result_file + "channel.txt"
        try:
            ch = open(ch_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for channel in ch:
                L.append(channel)
            for i in range(len(L)):
                Channel.append(L[i].strip())
            return Channel
        except Exception as err:
            logger.info(err)
        finally:
            ch.close()

    @staticmethod
    def Att_get():
        L = []
        att_path = result_file + "attention.txt"
        try:
            att = open(att_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for attention in att:
                L.append(attention)
            for i in range(len(L)):
                Att_rep.append(int(L[i].strip().encode('utf-8')))
            return Att_rep
        except Exception as err:
            logger.info(err)
        finally:
            att.close()

    @staticmethod
    def Angle_get():
        L = []
        angle_path = result_file + "angle.txt"
        try:
            angle = open(angle_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for ag in angle:
                L.append(ag)
            for i in range(len(L)):
                Angle.append(L[i].strip().encode('utf-8'))
                #print('Angle list', Angle)
            return Angle
        except Exception as err:
            logger.info(err)
        finally:
            angle.close()

    @staticmethod
    def Tx_tp_get():
        L = []
        tx_tp_path = result_file + "tx_tp.txt"
        try:
            tx_tp = open(tx_tp_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for txthought in tx_tp:
                L.append(txthought)
            for i in range(len(L)):
                Tx_Throught.append(L[i].strip().encode('utf-8'))
            return Tx_Throught
        except Exception as err:
            logger.info(err)
        finally:
            tx_tp.close()

    @staticmethod
    def Rx_tp_get():
        L = []
        rx_tp_path = result_file + "rx_tp.txt"
        try:
            rx_tp = open(rx_tp_path)
            #print(rx_tp)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for rxthought in rx_tp:
                L.append(rxthought)
                #print(L)
            for i in range(len(L)):
                Rx_Throught.append(L[i].strip().encode('utf-8'))
            #print(Rx_Throught)
            return Rx_Throught
        except Exception as err:
            logger.info(err)
        finally:
            rx_tp.close()

    @staticmethod
    def Sta_rssi_get():
        L = []
        sta_rssi_path = result_file + "sta_rssi.txt"
        try:
            sta_rssi = open(sta_rssi_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for starssi in sta_rssi:
                L.append(starssi)
            for i in range(len(L)):
                Sta_Rssi.append(L[i].strip())
            return Sta_Rssi
        except Exception as err:
            logger.info(err)
        finally:
            sta_rssi.close()

    @staticmethod
    def Ap_rssi_get():
        L = []
        ap_rssi_path = result_file + "ap_rssi.txt"
        try:
            ap_rssi = open(ap_rssi_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for aprssi in ap_rssi:
                L.append(aprssi)
            for i in range(len(L)):
                Ap_Rssi.append(L[i].strip())
                #print(Ap_Rssi)
            return Ap_Rssi
        except Exception as err:
            logger.info(err)
        finally:
            ap_rssi.close()

    @staticmethod
    def Tx_rate_get():
        L = []
        tx_rate_path = result_file + "tx_linkrate.txt"
        try:
            tx_rate = open(tx_rate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for txrate in tx_rate:
                L.append(txrate)
            for i in range(len(L)):
                Tx_Rate.append(L[i].strip().encode('utf-8'))
            return Tx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            tx_rate.close()

    @staticmethod
    def Rx_rate_get():
        L = []
        rx_rate_path = result_file + "rx_linkrate.txt"
        try:
            rx_rate = open(rx_rate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for rxrate in rx_rate:
                L.append(rxrate)
            for i in range(len(L)):
                Rx_Rate.append(L[i].strip().encode('utf-8'))
            return Rx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            rx_rate.close()

    @staticmethod
    def Dura_Time_get():
        L = []
        dura_time_path = result_file + "test_time.txt"
        try:
            dura_time = open(dura_time_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for duratime in dura_time:
                L.append(duratime)
            for i in range(len(L)):
                Dura_Time.append(L[i].strip())
            return Dura_Time
        except Exception as err:
            logger.info(err)
        finally:
            dura_time.close()

    @staticmethod
    def MCS_TxRate_get():
        L = []
        mcs_txrate_path = result_file + "mcs_txrate.txt"
        try:
            mcs_txrate = open(mcs_txrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for mcstxrate in mcs_txrate:
                L.append(mcstxrate)
            for i in range(len(L)):
                MCS_Tx_Rate.append(L[i].strip())
            return MCS_Tx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            mcs_txrate.close()

    @staticmethod
    def MCS_RxRate_get():
        L = []
        mcs_rxrate_path = result_file + "mcs_rxrate.txt"
        try:
            mcs_rxrate = open(mcs_rxrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for mcsrxrate in mcs_rxrate:
                L.append(mcsrxrate)
            for i in range(len(L)):
                MCS_Rx_Rate.append(L[i].strip())
            return MCS_Rx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            mcs_rxrate.close()

    @staticmethod
    def NSS_TxRate_get():
        L = []
        nss_txrate_path = result_file + "nss_txrate.txt"
        try:
            nss_txrate = open(nss_txrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for nsstxrate in nss_txrate:
                L.append(nsstxrate)
            for i in range(len(L)):
                NSS_Tx_Rate.append(L[i].strip())
            return NSS_Tx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            nss_txrate.close()

    @staticmethod
    def NSS_RxRate_get():
        L = []
        nss_rxrate_path = result_file + "nss_rxrate.txt"
        try:
            nss_rxrate = open(nss_rxrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for nssrxrate in nss_rxrate:
                L.append(nssrxrate)
            for i in range(len(L)):
                NSS_Rx_Rate.append(L[i].strip())
            return NSS_Rx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            nss_rxrate.close()

    @staticmethod
    def BW_TxRate_get():
        L = []
        bw_txrate_path = result_file + "bw_txrate.txt"
        try:
            bw_txrate = open(bw_txrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for bwtxrate in bw_txrate:
                L.append(bwtxrate)
            for i in range(len(L)):
                BW_Tx_Rate.append(L[i].strip())
            return BW_Tx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            bw_txrate.close()

    @staticmethod
    def BW_RxRate_get():
        L = []
        bw_rxrate_path = result_file + "bw_rxrate.txt"
        try:
            bw_rxrate = open(bw_rxrate_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for bwrxrate in bw_rxrate:
                L.append(bwrxrate)
            for i in range(len(L)):
                BW_Rx_Rate.append(L[i].strip())
            return BW_Rx_Rate
        except Exception as err:
            logger.info(err)
        finally:
            bw_rxrate.close()

    @staticmethod
    def RSSI_TXANT_get():
        L = []
        rssi_txant_path = result_file + "rssi_txant.txt"
        try:
            rssi_txant = open(rssi_txant_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for rssitxant in rssi_txant:
                L.append(rssitxant)
            for i in range(len(L)):
                TX_RSSI_ANT.append(L[i].strip())
            return TX_RSSI_ANT
        except Exception as err:
            logger.info(err)
        finally:
            rssi_txant.close()

    @staticmethod
    def POWER_TXANT_get():
        L = []
        power_txant_path = result_file + "power_txant.txt"
        try:
            power_txant = open(power_txant_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for powertxant in power_txant:
                L.append(powertxant)
            for i in range(len(L)):
                TX_POWER_ANT.append(L[i].strip())
            return TX_POWER_ANT
        except Exception as err:
            logger.info(err)
        finally:
            power_txant.close()

    @staticmethod
    def RSSI_RXANT_get():
        L = []
        rssi_rxant_path = result_file + "rssi_rxant.txt"
        try:
            rssi_rxant = open(rssi_rxant_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for rssirxant in rssi_rxant:
                L.append(rssirxant)
            for i in range(len(L)):
                RX_RSSI_ANT.append(L[i].strip())
            return RX_RSSI_ANT
        except Exception as err:
            logger.info(err)
        finally:
            rssi_rxant.close()

    @staticmethod
    def POWER_RXANT_get():
        L = []
        power_rxant_path = result_file + "power_rxant.txt"
        try:
            power_rxant = open(power_rxant_path)
        except Exception as err:
            logger.info(err)
            exit(-1)
        try:
            for powerrxant in power_rxant:
                L.append(powerrxant)
            for i in range(len(L)):
                RX_POWER_ANT.append(L[i].strip())
            return RX_POWER_ANT
        except Exception as err:
            logger.info(err)
        finally:
            power_rxant.close()




if __name__ == "__main__":
    #os.chdir('..')
    retval = os.getcwd()
    print('DATA FILE', retval)
    Reportdata_Get.Rx_tp_get()
    print('XXXXXX', Rx_Throught)
    Reportdata_Get.Tx_tp_get()
    Reportdata_Get.Tx_rate_get()
    Reportdata_Get.Ap_rssi_get()
    Reportdata_Get.Rx_rate_get()
    Reportdata_Get.Sta_rssi_get()
    Reportdata_Get.Ch_get()
    Reportdata_Get.Att_get()
    Reportdata_Get.Angle_get()
    Reportdata_Get.Dura_Time_get()
    Reportdata_Get.MCS_TxRate_get()
    Reportdata_Get.MCS_RxRate_get()
    Reportdata_Get.NSS_TxRate_get()
    Reportdata_Get.NSS_RxRate_get()
    Reportdata_Get.BW_TxRate_get()
    Reportdata_Get.BW_RxRate_get()
    Reportdata_Get.RSSI_ANT_get()
    Reportdata_Get.POWER_ANT_get()
