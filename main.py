# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 15:19
# @Author  : Ethan
"""the main control, get the configure for entire test system
    """

import logging
import os
import shutil
import time
import threading
import win32api
import win32con

from config import Config, Con_current_atten, Con_current_angle
from switch import Switch
from throught import Throught
from att import Attenuate
from turntable import Turntable
from data.parameters import DUT_NAME, DUT_TYPE, DUT_IP, RADIO, DUT_USERNAME, DUT_PASSWORD, SSID, RADIO, CHANNEL, SERIAL_COM, SERIAL_BAUDRATE, \
    STA_TYPE, STA_IP, STA_USERNAME, STA_PASSWORD, STA_SERIAL_COM, STA_SERIAL_BAUDRATE, ATTENUATE_LIST, ATTEN_1_IP, \
    ANGLE_LIST, ANGLE_NUM, TABLE_IP, TABLE_COM, RUN_TPYE, ADAPTER, DUT_IPERF_EX, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, \
    DUT_EX2_USERNAME, DUT_EX2_PASSWORD, STA_IPERF_EX, STA_EX_USERNAME, STA_EX_PASSWORD, IPERF_PORT1, IPERF_PORT2, \
    PAIR, DURATION, DUT_IPERF_IP1, DUT_IPERF_IP2, STA_IPERF_IP1, STA_IPERF_IP2, TEST_DL, TEST_UL, DEBUG_LOG, SSH_PORT, \
    STA_SSH_PORT, SSH_EN, TELNET_EN, SERIAL_EN, ADB_EN, TELNET_PORT, STA_TELNET_PORT
from data.write_datas import dutinfo_write, channel_write, atten_write, angle_write, ap_rssi_write, tx_linkrate_write, \
    sta_rssi_write, rx_linkrate_write, mcs_txrate_write, mcs_rxrate_write, nss_txrate_write, nss_rxrate_write, \
    bw_txrate_write, bw_rxrate_write, rssi_txant_write, power_txant_write, rssi_rxant_write, power_rxant_write, tx_tp_wirte, rx_tp_write
from report import Generate_Test_Report
from rssi_product import product_RSSI_telnet, product_RSSI_ssh, product_RSSI_serial, product_RSSI_adb
from rssi import get_BSSI
from iper import server_run, iperf3_client, iperf3_client_localDL, iperf3_client_localUL
from wifi_netsh import wifi_ssh, wifi_local
# from switch import Switch
# from pdv_dll import PDV
import logging
logger = logging.getLogger()
console_handler = logging.StreamHandler()

#create a handler 
log_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
file_handler = logging.FileHandler('./log/log_'+log_time+'.txt', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
        logging.Formatter(
                fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        )
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
if DEBUG_LOG == '1':
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
        logging.Formatter(
                fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        )
logger.addHandler(console_handler)


SERIAL_COM = 'COM' + SERIAL_COM

def create_result_folder():
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    retval = os.getcwd()
    result_file = retval + '/Result/Data/' + DUT_NAME + '_' + RADIO + '/'
    iperf3_file = retval + '/Result/iperf3/' + DUT_NAME +  '_' + RADIO + '/'
    result_file_name = retval + '/Result/Data/' + DUT_NAME + '_' + RADIO
    iperf3_file_name = retval + '/Result/iperf3/' + DUT_NAME + '_' + RADIO
    # win32api.MessageBox(0, "测试开始前会备份和测试项目名称一致的数据文件夹(Result)，若数据有用，请备份后再点击确认开始测试\r\n"
    #                        "When the test start, it will delete the result file,"
    #                        " Please transport your test result firstly!", "Warning", win32con.MB_OK)
    # logger.warning('When the test start, it will delete the result file,Please transport your test result firstly!')

    isExists_rf = os.path.exists(result_file)
    isExists_if = os.path.exists(iperf3_file)
    if not isExists_rf:
        os.makedirs(result_file)
        logger.info(result_file + ' Create Success')
    else:
        # logger.info(result_file + ' file is exist, delete and create new')
        # shutil.rmtree(result_file)
        # os.makedirs(result_file)
        shutil.move(result_file,result_file_name+'_'+now_time)
        os.makedirs(result_file)


    if not isExists_if:
        os.makedirs(iperf3_file)
        logger.info(iperf3_file + ' Create Success')
    else:
        # logger.info(iperf3_file + ' file is exist, delete and create new')
        # shutil.rmtree(iperf3_file)
        # os.makedirs(iperf3_file)
        shutil.move(iperf3_file, iperf3_file_name+'_'+now_time)
        os.makedirs(iperf3_file)

def check_connection():
    if STA_TYPE == 'AC88' or STA_TYPE == 'AX210' or STA_TYPE == 'BE865':
        conn_times = 0
        while conn_times < 3:
            try:
                wifi_local(SSID, ADAPTER, STA_IP)
            except Exception as err:
                conn_times += 1
                logger.error(err+SSID+'Wireless Card Connect Fail, Try again '+ conn_times)
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IP)
                    if ping_result == '1':
                        logger.error('ping ' +DUT_NAME + ' fail, Please Check.' +err)
                        exit()
                    else:
                        logger.info('Connect Success, Start Test.')
                        conn_times += 3
                except Exception as err:
                    logger.error(err)
                    exit()
    elif STA_TYPE == 'DEMO':
        try:
            ping_result = os.system('ping %s' % DUT_IP)
            if ping_result == '1':
                logger.error('ping' +DUT_NAME + 'fail, Please Check.' +err)
                exit()
            else:
                'Connect Success, Start Test.'
        except Exception as err:
            logger.error(err)
    else:
        logger.error('Pls Check your Station type paramters configration.')
        exit(-1)

def iperf_DL(att, angle):
    if DUT_IPERF_EX == '0' and STA_IPERF_EX == '0':
        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
            port = IPERF_PORT1
        elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
            port = IPERF_PORT2
        else:
            port = '5201'
        # port1 = port2 = port
        # server1_ip = server2_ip = DUT_IP
        # client1_ip = client2_ip = STA_IP
        try:
            server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port)
        except Exception as err:
            logger.error(err)
        else:
            time.sleep(1)
            try:
                client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
            except Exception as err:
                logger.error(err)
            else:
                client_run.iper_DL(DUT_IP, STA_IP, port, att, angle)
                logger.info('Test Done')  
    elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % STA_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
            else:
                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                    port = IPERF_PORT1
                elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                    port = IPERF_PORT2
                else:
                    port = '5201'
                # port1 = port2 = port
                # server1_ip = server2_ip = DUT_IP
                # client1_ip = client2_ip = STA_IPERF_IP1
                try:
                    server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port)
                except Exception as err:
                    logger.error(err)
                else:
                    time.sleep(1)
                    try:
                        iperf3_client_localDL(DUT_IP, STA_IPERF_IP1, port, att, angle)
                    except Exception as err:
                        logger.error(err)
                    else:
                        logger.info('Test Done')        
    elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % STA_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.') 
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT1
                            port2 = IPERF_PORT2
                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                            port1 = IPERF_PORT1
                            port2  = int(IPERF_PORT1) + 1
                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT2
                            port2 = int(IPERF_PORT2) + 1 
                        else:
                            port1 = '5201'
                            port2 = '5202'
                        # server1_ip = server2_ip = DUT_IP
                        # client1_ip = STA_IPERF_IP1
                        # client2_ip = STA_IPERF_IP2
                        try:
                            server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port1)
                            time.sleep(1)
                            server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port2)
                            time.sleep(1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            try:
                                iperf3_client_localDL(DUT_IP, STA_IPERF_IP1, port1, att, angle)
                            except Exception as err:
                                logger.error(err)
                            else:
                                time.sleep(1)
                                client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                client_run.iper_DL(DUT_IP, STA_IPERF_IP2, port2, att, angle)
                                logger.info('Test Done')
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '0':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                    port = IPERF_PORT1
                elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                    port = IPERF_PORT2
                else:
                    port = '5201'
                # port1 = port2 = port
                # server1_ip = server2_ip = DUT_IPERF_IP1
                # client1_ip = client2_ip = STA_IP
                try:
                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                except Exception as err:
                    logger.error(err)
                else:
                    time.sleep(1)
                    try:
                        client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
                    except Exception as err:
                        logger.error(err)
                    else:
                        client_run.iper_DL(DUT_IPERF_IP1, STA_IP, port, att, angle)
                        logger.info('Test Done')           
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP1)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                            port = IPERF_PORT1
                        elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port = IPERF_PORT2
                        else:
                            port = '5201'
                        # port1 = port2 = port
                        # server1_ip = server2_ip = DUT_IPERF_IP1
                        # client1_ip = client2_ip = STA_IPERF_IP1
                        try:
                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port)
                        except Exception as err:
                            logger.error(err)
                        else:
                            time.sleep(1)
                            try:
                                iperf3_client_localDL(DUT_IPERF_IP1, STA_IPERF_IP1,port, att, angle)
                            except Exception as err:
                                logger.error(err)
                            else:
                                logger.info('Test Done') 
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP1)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP2)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.')
                            else:
                                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT1
                                    port2 = IPERF_PORT2
                                elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                    port1 = IPERF_PORT1
                                    port2  = int(IPERF_PORT1) + 1
                                elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT2
                                    port2 = int(IPERF_PORT2) + 1 
                                else:
                                    port1 = '5201'
                                    PORT2 = '5202'
                                # server1_ip = server2_ip = DUT_IPERF_IP1
                                # client1_ip = STA_IPERF_IP1
                                # client2_ip = STA_IPERF_IP2
                                try:
                                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    time.sleep(1)
                                    try:
                                        iperf3_client_localDL(DUT_IPERF_IP1, STA_IPERF_IP1, port1, att, angle)
                                    except Exception as err:
                                        logger.error(err)
                                    else:
                                        time.sleep(1)
                                        try:
                                            client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                        except Exception as err:
                                            logger.error(err)
                                        else:
                                            client_run.iper_DL(DUT_IPERF_IP1, STA_IPERF_IP2, port2, att, angle)
                                            logger.info('Test Done')
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '0':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT1
                            port2 = IPERF_PORT2
                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                            port1 = IPERF_PORT1
                            port2  = int(IPERF_PORT1) + 1
                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT2
                            port2 = int(IPERF_PORT2) + 1 
                        else:
                            port1 = '5201'
                            port2 = '5202'
                        # server1_ip = DUT_IPERF_IP1
                        # server2_ip = DUT_IPERF_IP2
                        # client1_ip = client2_ip = STA_IP
                        try:
                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                            server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                        except Exception as err:
                            logger.error(err)
                        else:
                            try:
                                client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
                            except Exception as err:
                                logger.error(err)
                            else:
                                try:
                                    client_run.iper_DL(DUT_IPERF_IP1, STA_IP, port1, att, angle)
                                    client_run.iper_DL(DUT_IPERF_IP2, STA_IP, port2, att, angle)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    logger.info('Test Done')       
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                            else:
                                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT1
                                    port2 = IPERF_PORT2
                                elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                    port1 = IPERF_PORT1
                                    port2  = int(IPERF_PORT1) + 1
                                elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT2
                                    port2 = int(IPERF_PORT2) + 1 
                                else:
                                    port1 = '5201'
                                    port2 = '5202'
                                # server1_ip = DUT_IPERF_IP1
                                # server2_ip = DUT_IPERF_IP2
                                # client1_ip = client2_ip = STA_IPERF_IP1
                                # server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                # server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                # iperf3_client_localDL(DUT_IPERF_IP1,port1, att, angle)
                                # iperf3_client_localDL(DUT_IPERF_IP2, port2, att, angle)
                                # logger.info('Test Done')
                                # try:
                                #     server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                #     server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                # except Exception as err:
                                #     logger.error(err)
                                # else:
                                #     try:
                                #         iperf3_client_localDL(DUT_IPERF_IP1, STA_IPERF_IP1,port1, att, angle)
                                #         iperf3_client_localDL(DUT_IPERF_IP2, STA_IPERF_IP1,port2, att, angle)
                                #     except Exception as err:
                                #         logger.error(err)
                                #     else:
                                #         logger.info('Test Done')    
                                try:
                                    threads_server = []
                                    threads_server.append(threading.Thread(target=server_run,args=(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)))
                                    threads_server.append(threading.Thread(target=server_run,args=(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)))
                                    logger.debug(threads_server)
                                    for server in threads_server:
                                        logger.debug(server)
                                        server.start()
                                    for server in threads_server:
                                        server.join()
                                    # server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                    # server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    try:
                                        threads_client = []
                                        threads_client.append(threading.Thread(target=iperf3_client_localDL,args=(DUT_IPERF_IP1, STA_IPERF_IP1,port1,att, angle)))
                                        threads_client.append(threading.Thread(target=iperf3_client_localDL,args=(DUT_IPERF_IP2, STA_IPERF_IP1,port2, att, angle)))
                                        logger.debug(threads_client)
                                        for client in threads_client:
                                            logger.debug(client)
                                            client.start()
                                        for client in threads_client:
                                            client.join()
                                        # iperf3_client_localUL(DUT_IPERF_IP1, STA_IPERF_IP1,port1,att, angle)
                                        # iperf3_client_localUL(DUT_IPERF_IP2, STA_IPERF_IP1,port2, att, angle)
                                    except Exception as err:
                                        logger.error(err)
                                    else:
                                        logger.info('Test Done')                   
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                            else:
                                try:
                                    ping_result = os.system('ping %s' % STA_IPERF_IP2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    if ping_result == '1':
                                        logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.')
                                    else:
                                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                            port1 = IPERF_PORT1
                                            port2 = IPERF_PORT2
                                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                            port1 = IPERF_PORT1
                                            port2  = int(IPERF_PORT1) + 1
                                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                            port1 = IPERF_PORT2
                                            port2 = int(IPERF_PORT2) + 1 
                                        else:
                                            port1 = '5201'
                                            port2 = '5202'
                                        # server1_ip = DUT_IPERF_IP1
                                        # server2_ip = DUT_IPERF_IP2
                                        # client1_ip = STA_IPERF_IP1
                                        # client2_ip = STA_IPERF_IP2
                                        try:
                                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                            server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                        except Exception as err:
                                            logger.error(err)
                                        else:
                                            try:
                                                iperf3_client_localDL(DUT_IPERF_IP1, STA_IPERF_IP1, port1, att, angle)
                                            except Exception as err:
                                                logger.error(err)
                                            else:
                                                try:
                                                    client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                                except Exception as err:
                                                    logger.error(err)
                                                else:
                                                    client_run.iper_DL(DUT_IPERF_IP2, STA_IPERF_IP2, port2, att, angle)
                                                    logger.info('Test Done')    

def iperf_UL(att, angle):
    if DUT_IPERF_EX == '0' and STA_IPERF_EX == '0':
        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
            port = IPERF_PORT1
        elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
            port = IPERF_PORT2
        else:
            port = '5201'
        # port1 = port2 = port
        # server1_ip = server2_ip = DUT_IP
        # client1_ip = client2_ip = STA_IP
        server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port)
        time.sleep(1)
        client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
        client_run.iper_UL(DUT_IP, STA_IP,port, att, angle)
        logger.info('Test Done')  
    elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % STA_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
            else:
                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                    port = IPERF_PORT1
                elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                    port = IPERF_PORT2
                else:
                    port = '5201'
                # port1 = port2 = port
                # server1_ip = server2_ip = DUT_IP
                # client1_ip = client2_ip = STA_IPERF_IP1
                try:
                    server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port)
                except Exception as err:
                    logger.error(err)
                else:
                    time.sleep(1)
                    try:
                        iperf3_client_localUL(DUT_IP, STA_IPERF_IP1, port, att, angle)
                    except Exception as err:
                        logger.error(err)
                    else:
                        logger.info('Test Done')        
    elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % STA_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.') 
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT1
                            port2 = IPERF_PORT2
                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                            port1 = IPERF_PORT1
                            port2  = int(IPERF_PORT1) + 1
                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT2
                            port2 = int(IPERF_PORT2) + 1 
                        else:
                            port1 = '5201'
                            port2 = '5202'
                        # server1_ip = server2_ip = DUT_IP
                        # client1_ip = STA_IPERF_IP1
                        # client2_ip = STA_IPERF_IP2
                        try:
                            server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port1)
                            time.sleep(1)
                            server_run(DUT_IP, DUT_USERNAME, DUT_PASSWORD, port2)
                            time.sleep(1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            try:
                                iperf3_client_localUL(DUT_IP, STA_IPERF_IP1,port1,att,angle)
                            except Exception as err:
                                logger.error(err)
                            else:
                                time.sleep(1)
                                try:
                                    client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    client_run.iper_UL(DUT_IP, STA_IPERF_IP2,port2, att, angle)
                                    logger.info('Test Done')
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '0':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                    port = IPERF_PORT1
                elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                    port = IPERF_PORT2
                else:
                    port = '5201'
                # port1 = port2 = port
                # server1_ip = server2_ip = DUT_IPERF_IP1
                # client1_ip = client2_ip = STA_IP
                try:
                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                except Exception as err:
                    logger.error(err)
                else:
                    time.sleep(1)
                    try:
                        client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
                    except Exception as err:
                        logger.error(err)
                    else:
                        try:
                            client_run.iper_UL(DUT_IPERF_IP1, STA_IP, port, att, angle)
                        except Exception as err:
                            logger.error(err)
                        else:
                            logger.info('Test Done')           
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP1)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True:
                            port = IPERF_PORT1
                        elif IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port = IPERF_PORT2
                        else:
                            port = '5201'
                        # port1 = port2 = port
                        # server1_ip = server2_ip = DUT_IPERF_IP1
                        # client1_ip = client2_ip = STA_IPERF_IP1
                        try:
                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port)
                        except Exception as err:
                            logger.error(err)
                        else:
                            time.sleep(1)
                            try:
                                iperf3_client_localUL(DUT_IPERF_IP1, STA_IPERF_IP1,port,att,angle)
                            except Exception as err:
                                logger.error(err)
                            else:
                                logger.info('Test Done') 
    elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % STA_IPERF_IP1)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP2)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.')
                            else:
                                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT1
                                    port2 = IPERF_PORT2
                                elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                    port1 = IPERF_PORT1
                                    port2  = int(IPERF_PORT1) + 1
                                elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT2
                                    port2 = int(IPERF_PORT2) + 1 
                                else:
                                    port1 = '5201'
                                    PORT2 = '5202'
                                # server1_ip = server2_ip = DUT_IPERF_IP1
                                # client1_ip = STA_IPERF_IP1
                                # client2_ip = STA_IPERF_IP2
                                try:
                                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                    server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    time.sleep(1)
                                    try:
                                        iperf3_client_localUL(DUT_IPERF_IP1,STA_IPERF_IP1,port1,att,angle)
                                    except Exception as err:
                                        logger.error(err)
                                    else:
                                        time.sleep(1)
                                        try:
                                            client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                        except Exception as err:
                                            logger.error(err)
                                        else:
                                            client_run.iper_UL(DUT_IPERF_IP1, STA_IPERF_IP2,port2, att, angle)
                                            logger.info('Test Done')
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '0':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT1
                            port2 = IPERF_PORT2
                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                            port1 = IPERF_PORT1
                            port2  = int(IPERF_PORT1) + 1
                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                            port1 = IPERF_PORT2
                            port2 = int(IPERF_PORT2) + 1 
                        else:
                            port1 = '5201'
                            port2 = '5202'
                        # server1_ip = DUT_IPERF_IP1
                        # server2_ip = DUT_IPERF_IP2
                        # client1_ip = client2_ip = STA_IP
                        try:
                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                            server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                        except Exception as err:
                            logger.error(err)
                        else:
                            try:
                                client_run = iperf3_client(STA_IP, STA_USERNAME, STA_PASSWORD)
                            except Exception as err:
                                logger.error(err)
                            else:
                                try:
                                    client_run.iper_UL(DUT_IPERF_IP1, STA_IP, port1, att, angle)
                                    client_run.iper_UL(DUT_IPERF_IP2, STA_IP, port2, att, angle)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    logger.info('Test Done')       
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '1':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                            else:
                                if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT1
                                    port2 = IPERF_PORT2
                                elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                    port1 = IPERF_PORT1
                                    port2  = int(IPERF_PORT1) + 1
                                elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                    port1 = IPERF_PORT2
                                    port2 = int(IPERF_PORT2) + 1 
                                else:
                                    port1 = '5201'
                                    port2 = '5202'
                                # server1_ip = DUT_IPERF_IP1
                                # server2_ip = DUT_IPERF_IP2
                                # client1_ip = client2_ip = STA_IPERF_IP1
                                try:
                                    threads_server = []
                                    threads_server.append(threading.Thread(target=server_run,args=(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)))
                                    threads_server.append(threading.Thread(target=server_run,args=(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)))
                                    logger.debug(threads_server)
                                    for server in threads_server:
                                        logger.debug(server)
                                        server.start()
                                    for server in threads_server:
                                        server.join()
                                    # server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                    # server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    try:
                                        threads_client = []
                                        threads_client.append(threading.Thread(target=iperf3_client_localUL,args=(DUT_IPERF_IP1, STA_IPERF_IP1,port1,att, angle)))
                                        threads_client.append(threading.Thread(target=iperf3_client_localUL,args=(DUT_IPERF_IP2, STA_IPERF_IP1,port2, att, angle)))
                                        logger.debug(threads_client)
                                        for client in threads_client:
                                            logger.debug(client)
                                            client.start()
                                        for client in threads_client:
                                            client.join()
                                        # iperf3_client_localUL(DUT_IPERF_IP1, STA_IPERF_IP1,port1,att, angle)
                                        # iperf3_client_localUL(DUT_IPERF_IP2, STA_IPERF_IP1,port2, att, angle)
                                    except Exception as err:
                                        logger.error(err)
                                    else:
                                        logger.info('Test Done')        
    elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '2':
        try:
            ping_result = os.system('ping %s' % DUT_IPERF_IP1)
        except Exception as err:
            logger.error(err)
        else:
            if ping_result == '1':
                logger.error('ping' + DUT_IPERF_IP1 + 'fail, Please Check.')
            else:
                try:
                    ping_result = os.system('ping %s' % DUT_IPERF_IP2)
                except Exception as err:
                    logger.error(err)
                else:
                    if ping_result == '1':
                        logger.error('ping' + DUT_IPERF_IP2 + 'fail, Please Check.')
                    else:
                        try:
                            ping_result = os.system('ping %s' % STA_IPERF_IP1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            if ping_result == '1':
                                logger.error('ping' + STA_IPERF_IP1 + 'fail, Please Check.')
                            else:
                                try:
                                    ping_result = os.system('ping %s' % STA_IPERF_IP2)
                                except Exception as err:
                                    logger.error(err)
                                else:
                                    if ping_result == '1':
                                        logger.error('ping' + STA_IPERF_IP2 + 'fail, Please Check.')
                                    else:
                                        if IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                            port1 = IPERF_PORT1
                                            port2 = IPERF_PORT2
                                        elif IPERF_PORT1 is not None and str(IPERF_PORT1).isdigit() is True and IPERF_PORT2 is None:
                                            port1 = IPERF_PORT1
                                            port2  = int(IPERF_PORT1) + 1
                                        elif IPERF_PORT1 is None and IPERF_PORT2 is not None and str(IPERF_PORT2).isdigit() is True:
                                            port1 = IPERF_PORT2
                                            port2 = int(IPERF_PORT2) + 1 
                                        else:
                                            port1 = '5201'
                                            port2 = '5202'
                                        # server1_ip = DUT_IPERF_IP1
                                        # server2_ip = DUT_IPERF_IP2
                                        # client1_ip = STA_IPERF_IP1
                                        # client2_ip = STA_IPERF_IP2
                                        try:
                                            server_run(DUT_IPERF_IP1, DUT_EX1_USERNAME, DUT_EX1_PASSWORD, port1)
                                            server_run(DUT_IPERF_IP2, DUT_EX2_USERNAME, DUT_EX2_PASSWORD, port2)
                                        except Exception as err:
                                            logger.error(err)
                                        else:
                                            try:
                                                iperf3_client_localUL(DUT_IPERF_IP1, STA_IPERF_IP1,port1,att, angle)
                                            except Exception as err:
                                                logger.error(err)
                                            else:
                                                try:
                                                    client_run = iperf3_client(STA_IPERF_IP2, STA_EX_USERNAME, STA_EX_PASSWORD)
                                                except Exception as err:
                                                    logger.error(err)
                                                else:
                                                    try:
                                                        client_run.iper_UL(DUT_IPERF_IP2, STA_IPERF_IP2,port2, att, angle)
                                                    except Exception as err:
                                                        logger.error(err)
                                                    else:
                                                        logger.info('Test Done')  

def test():
    # # set swivel table
    # # wait_table_time = set_swivel_table(ANGLE_NUM, TABLE_COM, 'clockwise')
    # set run type OTA or Conductive
    if STA_TYPE == 'AC88':
        # Condctive 4x4 11ac
        # swt = Switch(STA_SWITCHIP)
        # swt.set_default()
        swt = Switch('10.1.0.12')
        swt.set_default()
        swt.set_switch_runtype()
    # #test
    # swivel table set to default
    if RUN_TPYE == 0 and ANGLE_NUM > 1:
        try:
            logger.debug(TABLE_IP)
            ping_result = os.system('ping %s' % TABLE_IP)
            if ping_result == '1':
                logger.error('ping Turntable fail, Please Check.')
                exit(0)
            else:
                try:
                    table = Turntable(TABLE_IP)
                except Exception as err:
                    logger.error(err)
                else:
                    logger.info('Connect turntable Success, adjust turntable.')                    
                    table.set_default()
                    logger.info('Waiting for swivel table back to zero...!!!Please check the DUT status!!!')
                    time.sleep(60)
        except Exception as err:
            logger.error(err)
    for i in ATTENUATE_LIST:
        # set fixed or ota att
        logger.info(f'ATT:{i}')
        retval = os.getcwd()
        logger.debug(f'path check:{retval}')
        att_set_config = Con_current_atten(i)
        att_set_config.write_atten()
        logger.debug(ATTEN_1_IP)
        try:
            ping_result = os.system('ping %s' % ATTEN_1_IP)
            if ping_result == '1':
                logger.error('ping Atten fail, Please Check.')
                exit(0)
            else:
                logger.info('Connect att Success, adjust att.')
                try:
                    att = Attenuate(ATTEN_1_IP)
                except Exception as err:
                    logger.error(err)    
                else:
                    # att.login('user 1','')
                    # att.set_default()
                    att.set_att(i)
                    att.close()
        except Exception as err:
            logger.error(err)
        # # print(type(RUN_TPYE),type(CHANNEL)),real att
        # if RUN_TPYE == 0 and CHANNEL < 20:
        #     real_att = i + 62
        # elif RUN_TPYE == 0 and CHANNEL > 30:
        #     real_att = i + 76
        # elif RUN_TPYE == 1 and CHANNEL < 20:
        #     real_att = i + 22
        # elif RUN_TPYE == 1 and CHANNEL > 30:
        #     real_att = i + 28
        # print(type(RUN_TPYE),type(CHANNEL)),aten att
        real_att = i
        atten_write(str(real_att))
        logger.info('Wait for single good!')
        time.sleep(2)
        check_connection()
        # GET DUT INFO
        if SSH_EN == 1:
            try:
                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                dut_sn, hw_version, sw_version = P_ap.get_dut_info()
                dutinfo_write(dut_sn+','+hw_version+','+sw_version)
                P_ap.close()
            except:
                logger.error('No dutinfo')
                dut_sn = hw_version = sw_version = ''
        # get channel
        channel_write(str(CHANNEL))
        # print('xxx',ANGLE_LIST)
        for x in ANGLE_LIST:
            logger.info(f'ANGLE:{x}')
            retval = os.getcwd()
            logger.debug(f'path check:{retval}')
            angle_set_config = Con_current_angle(x)
            angle_set_config.write_angle()
            angle_write(str(x))
            if RUN_TPYE == 0 and ANGLE_NUM > 1:
                table.set_angle(x)
                logger.info('Angle:'+str(x))
                wait_table_time = 36/int(ANGLE_NUM)
                time.sleep(wait_table_time)
            # else:
            #     logger.info('Angle:'+str(x))
            
            # get RSSI and link rate info
            if DUT_TYPE == 'QCA':
                if STA_TYPE == 'AX210' or STA_TYPE == 'AC88' or STA_TYPE == 'BE865':
                    # get DL counts
                    def get_statistics_tx():
                        time.sleep(10)
                        try:
                            sta_rssi = get_BSSI(SSID)
                        except Exception as err:
                            logger.error(err)
                        else:
                            sta_rssi_write(str(sta_rssi).strip())
                    # get UL counts
                    def get_statistics_rx():
                        time.sleep(10)
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # get radio id
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = P_ap.get_APRSSI_qca(RADIO, iwface)
                            ap_rssi_nouse, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                                P_ap.get_rxcounts_qca(ifface)
                            # write ap's rssi and linkrate
                            ap_rssi_write(str(ap_rssi).strip())
                            rx_linkrate_write(str(rx_link_rate).strip())
                            # power_rxant_write(str(sta_power).strip())
                            rssi_rxant_write(str(ap_rssi_chain0).strip() +'|'+ str(ap_rssi_chain1).strip() +'|'+
                                            str(ap_rssi_chain2).strip() +'|'+ str(ap_rssi_chain3).strip() +'|'+
                                            str(ap_rssi_chain4).strip() +'|'+ str(ap_rssi_chain5).strip() +'|'+
                                            str(ap_rssi_chain6).strip() +'|'+ str(ap_rssi_chain7).strip())
                            P_ap.close()

                        # main test
                    # tx
                    if TEST_DL == 1:
                        # print(SSH_PORT,type(SSH_PORT))
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            P_ap.qca_reset(iwface, ifface)
                            P_ap.close()
                            # run iperf3 and get rssi
                            threads_tx = []
                            threads_tx.append(threading.Thread(target=iperf_DL,args=(i,x)))
                            threads_tx.append(threading.Thread(target=get_statistics_tx))
                            logger.debug(threads_tx)
                            for tx in threads_tx:
                                logger.debug(tx)
                                tx.start()
                            for tx in threads_tx:
                                tx.join()
                        # get counts
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = P_ap.get_APRSSI_qca(RADIO, iwface)
                            tx_power, tx_mcs, tx_nss, tx_bw = P_ap.get_txcounts_qca(iwface, ifface)
                            # write data
                            tx_linkrate_write(str(tx_link_rate).strip())
                            mcs_txrate_write(str(tx_mcs).strip())
                            nss_txrate_write(str(tx_nss).strip())
                            bw_txrate_write(str(tx_bw).strip())
                            power_txant_write(str(tx_power).strip())
                            P_ap.close()

                    if TEST_UL == 1:
                        # rx
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            P_ap.qca_reset(iwface, ifface)
                            P_ap.close()
                            # run chariot and get rssi
                            threads_rx = []
                            threads_rx.append(threading.Thread(target=iperf_UL,args=(i,x)))
                            threads_rx.append(threading.Thread(target=get_statistics_rx))
                            logger.debug(threads_rx)
                            for rx in threads_rx:
                                logger.debug(rx)
                                rx.start()
                            for rx in threads_rx:
                                rx.join()

                        # write
                        # write ap's rssi and linkrate
                        # get counts
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            ap_rssi, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, \
                                ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                                P_ap.get_rxcounts_qca(ifface)
                            # write data
                            mcs_rxrate_write(str(rx_mcs).strip())
                            nss_rxrate_write(str(rx_nss).strip())
                            bw_rxrate_write(str(rx_bw).strip())
                            P_ap.close()
                elif STA_TYPE == 'DEMO':
                    def get_statistics_tx():
                        time.sleep(10)
                        # get  info
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            # get radio id
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = \
                                P_ap.get_APRSSI_qca(RADIO, iwface)
                            # write ap's rssi and linkrate
                            # ap_rssi_write(str(ap_rssi).strip())
                            channel_write(str(get_channel))
                            tx_linkrate_write(str(tx_link_rate).strip())
                            # power_txant_write(str(ap_power).strip())
                            P_ap.close()
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_ssh(STA_IP, STA_SSH_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_serial(STA_IP, STA_SERIAL_COM, STA_SERIAL_BAUDRATE, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_sta = product_RSSI_telnet(STA_IP, STA_TELNET_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_sta = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_sta.get_testradio_qca(SSID)
                            sta_rssi, tx_mcs, tx_nss, tx_bw, sta_rssi_chain0, sta_rssi_chain1, sta_rssi_chain2, \
                                sta_rssi_chain3, sta_rssi_chain4, sta_rssi_chain5, sta_rssi_chain6, sta_rssi_chain7 = \
                                P_sta.get_rxcounts_qca(ifface)
                            sta_rssi_write(str(sta_rssi).strip())
                            rssi_txant_write(str(sta_rssi_chain0).strip() + str(sta_rssi_chain1).strip() +
                                            str(sta_rssi_chain2).strip() + str(sta_rssi_chain3).strip() +
                                            str(sta_rssi_chain4).strip() + str(sta_rssi_chain5).strip() +
                                            str(sta_rssi_chain6).strip() + str(sta_rssi_chain7).strip())
                            P_sta.close()

                    def get_statistics_rx():
                        time.sleep(10)
                        # get  info
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            # get radio id
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = \
                                P_ap.get_APRSSI_qca(RADIO, iwface)
                            ap_rssi_nouse, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, \
                                ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                                P_ap.get_rxcounts_qca(ifface)
                            # write ap's rssi and linkrate
                            ap_rssi_write(str(ap_rssi).strip())
                            rx_linkrate_write(str(rx_link_rate).strip())
                            # power_rxant_write(str(sta_power).strip())
                            rssi_rxant_write(str(ap_rssi_chain0).strip() + str(ap_rssi_chain1).strip() +
                                            str(ap_rssi_chain2).strip() + str(ap_rssi_chain3).strip() +
                                            str(ap_rssi_chain4).strip() + str(ap_rssi_chain5).strip() +
                                            str(ap_rssi_chain6).strip() + str(ap_rssi_chain7).strip())
                            P_ap.close()

                    # main
                    if TEST_DL == 1:
                        try:
                            # tx
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_ssh(STA_IP, STA_SSH_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_serial(STA_IP, STA_SERIAL_COM, STA_SERIAL_BAUDRATE, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_sta = product_RSSI_telnet(STA_IP, STA_TELNET_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_sta = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            iwface, ifface = P_sta.get_testradio_qca(SSID)
                            P_sta.qca_reset(iwface, ifface)
                            P_sta.close()
                            # run IPERF and get rssi
                            threads_tx = []
                            threads_tx.append(threading.Thread(target=iperf_DL,args=(i,x)))
                            threads_tx.append(threading.Thread(target=get_statistics_tx))
                            logger.debug(threads_tx)
                            for tx in threads_tx:
                                logger.debug(tx)
                                tx.start()
                            for tx in threads_tx:
                                tx.join()
                    # get counts
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_sta = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_sta = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_sta.get_testradio_qca(SSID)
                            sta_rssi, tx_mcs, tx_nss, tx_bw, sta_rssi_chain0, sta_rssi_chain1, sta_rssi_chain2, \
                                sta_rssi_chain3, sta_rssi_chain4, sta_rssi_chain5, sta_rssi_chain6, sta_rssi_chain7 = \
                                P_sta.get_rxcounts_qca(ifface)
                            # write data
                            mcs_txrate_write(str(tx_mcs).strip())
                            nss_txrate_write(str(tx_nss).strip())
                            bw_txrate_write(str(tx_bw).strip())
                            P_sta.close()

                    # rx
                    if TEST_UL == 1:
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            P_ap.qca_reset(iwface, ifface)
                            P_ap.close()
                            # run chariot and get rssi
                            threads_rx = []
                            threads_rx.append(threading.Thread(target=iperf_UL,args=(i,x)))
                            threads_rx.append(threading.Thread(target=get_statistics_rx))
                            logger.debug(threads_rx)
                            for rx in threads_rx:
                                logger.debug(rx)
                                rx.start()
                            for rx in threads_rx:
                                rx.join()

                        # write
                        # write ap's rssi and linkrate
                        # get counts
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_ap.get_testradio_qca(SSID)
                            ap_rssi, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, \
                                ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                                P_ap.get_rxcounts_qca(ifface)
                            # write data
                            mcs_rxrate_write(str(rx_mcs).strip())
                            nss_rxrate_write(str(rx_nss).strip())
                            bw_rxrate_write(str(rx_bw).strip())
                            P_ap.close()
            elif DUT_TYPE == 'MTK':
                if STA_TYPE == 'AX210' or STA_TYPE == 'AC88' or STA_TYPE == 'BE865':
                    # get DL counts
                    def get_statistics_tx():
                        time.sleep(10)
                        try:
                            sta_rssi = get_BSSI(SSID)
                        except Exception as err:
                            logger.error(err)
                        else:
                            sta_rssi_write(str(sta_rssi).strip())
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # get radio id
                            iface = P_ap.get_testradio_mtk(SSID)
                            aptx1_rssi, aptx2_rssi, aptx3_rssi, aptx4_rssi, aptx5_rssi,tx_mode, tx_bw, tx_nss, tx_mcs, tx_link_rate, rx_mode, rx_bw, rx_nss, rx_mcs, rx_link_rate = P_ap.get_APRSSI_mtk(RADIO, iface)
                            # tx_counts, rx_counts = P_ap.get_counts_mtk(RADIO, ap_radio_2g, ap_radio_5g)
                            # write data
                            tx_linkrate_write(str(tx_link_rate).strip())
                            mcs_txrate_write(str(tx_mcs).strip())
                            nss_txrate_write(str(tx_nss).strip())
                            bw_txrate_write(str(tx_mode+tx_bw).strip())
                            P_ap.close()
                    # get UL counts
                    def get_statistics_rx():
                        time.sleep(20)
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # get radio id
                            iface = P_ap.get_testradio_mtk(SSID)
                            aptx1_rssi, aptx2_rssi, aptx3_rssi, aptx4_rssi, aptx5_rssi,tx_mode, tx_bw, tx_nss, tx_mcs, tx_link_rate, rx_mode, rx_bw, rx_nss, rx_mcs, rx_link_rate = P_ap.get_APRSSI_mtk(RADIO, iface)
                            # tx_counts, rx_counts = P_ap.get_counts_mtk(RADIO, ap_radio_2g, ap_radio_5g)
                            # write ap's rssi and linkrate
                            ap_rssi_write(str('TX1:'+aptx1_rssi+',TX2:'+aptx2_rssi+',TX3:'+aptx3_rssi+',TX4:'+aptx4_rssi+',TX5:'+aptx5_rssi).strip())
                            rx_linkrate_write(str(rx_link_rate).strip())
                            mcs_rxrate_write(str(rx_mcs).strip())
                            nss_rxrate_write(str(rx_nss).strip())
                            bw_rxrate_write(str(rx_mode+rx_bw).strip())
                            # power_rxant_write(str(sta_power).strip())
                            rssi_rxant_write(str(aptx1_rssi).strip() + str(aptx2_rssi).strip() +
                                            str(aptx3_rssi).strip() + str(aptx4_rssi).strip() + str(aptx5_rssi).strip())
                            P_ap.close()
                    # tx
                    if TEST_DL == 1:
                        # print(SSH_PORT,type(SSH_PORT))
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            # dut_sn, hw_version, sw_version = P_ap.get_dut_info()
                            # dutinfo_write(dut_sn+','+hw_version+','+sw_version)
                            iface = P_ap.get_testradio_mtk(SSID)
                            P_ap.mtk_reset(iface)
                            P_ap.close()
                            # run iperf3 and get rssi
                            threads_tx = []
                            threads_tx.append(threading.Thread(target=iperf_DL,args=(i,x)))
                            threads_tx.append(threading.Thread(target=get_statistics_tx))
                            logger.debug(threads_tx)
                            for tx in threads_tx:
                                logger.debug(tx)
                                tx.start()
                            for tx in threads_tx:
                                tx.join()
                    # rx
                    if TEST_UL == 1:
                        # rx
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            P_ap.mtk_reset()
                            P_ap.close()
                            # run chariot and get rssi
                            threads_rx = []
                            threads_rx.append(threading.Thread(target=iperf_UL,args=(i,x)))
                            threads_rx.append(threading.Thread(target=get_statistics_rx))
                            logger.debug(threads_rx)
                            for rx in threads_rx:
                                logger.debug(rx)
                                rx.start()
                            for rx in threads_rx:
                                rx.join()
                elif STA_TYPE == 'DEMO':
                    def get_statistics_tx():
                        time.sleep(10)
                        try:
                            sta_rssi = get_BSSI(SSID)
                        except Exception as err:
                            logger.error(err)
                        else:
                            sta_rssi_write(str(sta_rssi).strip())
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # get radio id
                            iface = P_ap.get_testradio_mtk(SSID)
                            aptx1_rssi, aptx2_rssi, aptx3_rssi, aptx4_rssi, aptx5_rssi,tx_mode, tx_bw, tx_nss, tx_mcs, tx_link_rate, rx_mode, rx_bw, rx_nss, rx_mcs, rx_link_rate = P_ap.get_APRSSI_mtk(RADIO, iface)
                            # tx_counts, rx_counts = P_ap.get_counts_mtk(RADIO, ap_radio_2g, ap_radio_5g)
                            # write data
                            tx_linkrate_write(str(tx_link_rate).strip())
                            mcs_txrate_write(str(tx_mcs).strip())
                            nss_txrate_write(str(tx_nss).strip())
                            bw_txrate_write(str(tx_mode+tx_bw).strip())
                            P_ap.close()

                    def get_statistics_rx():
                        time.sleep(20)
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_ap.login(USER_NAME, PASSWORD)
                            # get radio id
                            iface = P_ap.get_testradio_mtk(SSID)
                            aptx1_rssi, aptx2_rssi, aptx3_rssi, aptx4_rssi, aptx5_rssi,tx_mode, tx_bw, tx_nss, tx_mcs, tx_link_rate, rx_mode, rx_bw, rx_nss, rx_mcs, rx_link_rate = P_ap.get_APRSSI_mtk(RADIO, iface)
                            # tx_counts, rx_counts = P_ap.get_counts_mtk(RADIO, ap_radio_2g, ap_radio_5g)
                            # write ap's rssi and linkrate
                            ap_rssi_write(str('TX1:'+aptx1_rssi+',TX2:'+aptx2_rssi+',TX3:'+aptx3_rssi+',TX4:'+aptx4_rssi+',TX5:'+aptx5_rssi).strip())
                            rx_linkrate_write(str(rx_link_rate).strip())
                            mcs_rxrate_write(str(rx_mcs).strip())
                            nss_rxrate_write(str(rx_nss).strip())
                            bw_rxrate_write(str(rx_mode+rx_bw).strip())
                            # power_rxant_write(str(sta_power).strip())
                            rssi_rxant_write(str(aptx1_rssi).strip() + str(aptx2_rssi).strip() +
                                            str(aptx3_rssi).strip() + str(aptx4_rssi).strip() + str(aptx5_rssi).strip())
                            P_ap.close()

                    # main
                    if TEST_DL == 1:
                        try:
                            # tx
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_ssh(STA_IP, STA_SSH_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_serial(STA_IP, STA_SERIAL_COM, STA_SERIAL_BAUDRATE, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_sta = product_RSSI_telnet(STA_IP, STA_TELNET_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_sta = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            # P_sta.login(STA_USERNAME, STA_PASSWORD)
                            iwface, ifface = P_sta.get_testradio_qca(SSID)
                            P_sta.qca_reset(iwface, ifface)
                            P_sta.close()
                            # run IPERF and get rssi
                            threads_tx = []
                            threads_tx.append(threading.Thread(target=iperf_DL,args=(i,x)))
                            threads_tx.append(threading.Thread(target=get_statistics_tx))
                            logger.debug(threads_tx)
                            for tx in threads_tx:
                                logger.debug(tx)
                                tx.start()
                            for tx in threads_tx:
                                tx.join()
                    # get counts
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_ssh(STA_IP, STA_SSH_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_sta = product_RSSI_serial(STA_IP, STA_SERIAL_COM, STA_SERIAL_BAUDRATE, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_sta = product_RSSI_telnet(STA_IP, STA_TELNET_PORT, STA_USERNAME, STA_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_sta = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            iwface, ifface = P_sta.get_testradio_qca(SSID)
                            sta_rssi, tx_mcs, tx_nss, tx_bw, sta_rssi_chain0, sta_rssi_chain1, sta_rssi_chain2, \
                                sta_rssi_chain3, sta_rssi_chain4, sta_rssi_chain5, sta_rssi_chain6, sta_rssi_chain7 = \
                                P_sta.get_rxcounts_qca(ifface)
                            # write data
                            mcs_txrate_write(str(tx_mcs).strip())
                            nss_txrate_write(str(tx_nss).strip())
                            bw_txrate_write(str(tx_bw).strip())
                            P_sta.close()

                    # rx
                    if TEST_UL == 1:
                        try:
                            if SSH_EN == 1 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_ssh(DUT_IP, SSH_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 1 and TELNET_EN == 0 and ADB_EN == 0:
                                P_ap = product_RSSI_serial(DUT_IP, SERIAL_COM, SERIAL_BAUDRATE, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 1 and ADB_EN == 0:
                                P_ap = product_RSSI_telnet(DUT_IP, TELNET_PORT, DUT_USERNAME, DUT_PASSWORD, RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 1:
                                P_ap = product_RSSI_adb(RADIO)
                            elif SSH_EN == 0 and SERIAL_EN == 0 and TELNET_EN == 0 and ADB_EN == 0:
                                pass
                            else:
                                logger.error('Please check the method for querying statistics!')
                                exit(-1)
                        except Exception as err:
                            logger.error(err)
                        else:
                            ifface = P_ap.get_testradio_mtk(SSID)
                            P_ap.mtk_reset(ifface)
                            P_ap.close()
                            # run chariot and get rssi
                            threads_rx = []
                            threads_rx.append(threading.Thread(target=iperf_UL,args=(i,x)))
                            threads_rx.append(threading.Thread(target=get_statistics_rx))
                            logger.debug(threads_rx)
                            for rx in threads_rx:
                                logger.debug(rx)
                                rx.start()
                            for rx in threads_rx:
                                rx.join()
                
            else:
                logger.debug('Unkown type')
                if TEST_DL == 1:
                    try:
                        iperf_DL(i,x)
                        # iperf_UL(i,x)
                    except:
                        logger.error('iperf can not run')
                if TEST_UL == 1:
                    try:
                        iperf_UL(i,x)
                    except:
                        logger.error('iperf can not run')

            # write tp value
            if TEST_DL == 1:
                if DUT_IPERF_EX == '0' and STA_IPERF_EX == '0':
                    server_ip = DUT_IP
                    client_ip = STA_IP
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput = throught.get_tx_throught_simple()
                    # rx_throughput = throught.get_rx_throught_simple()
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '1':
                    server_ip = DUT_IP
                    client_ip = STA_IPERF_IP1
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput = throught.get_tx_throught_simple()
                    # rx_throughput = throught.get_rx_throught_simple()
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta1 = throught.get_tx_throught_simple()
                    # rx_throughput_sta1 = throught.get_rx_throught_simple()
                    # rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta2 = throught.get_tx_throught_simple()
                    # rx_throughput_sta2 = throught.get_rx_throught_simple()
                    tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    # rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '0':
                    server_ip = DUT_IPERF_IP1
                    client_ip = STA_IP
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput = throught.get_tx_throught_simple()
                    # rx_throughput = throught.get_rx_throught_simple()
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '1':
                    server_ip = DUT_IPERF_IP1
                    client_ip = STA_IPERF_IP1
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput = throught.get_tx_throught_simple()
                    # rx_throughput = throught.get_rx_throught_simple()
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta1 = throught.get_tx_throught_simple()
                    # rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta2 = throught.get_tx_throught_simple()
                    # rx_throughput_sta2 = throught.get_rx_throught_simple()
                    tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    # rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '0':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IP) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IP) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta1 = throught.get_tx_throught_simple()
                    # rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IP) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IP) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta2 = throught.get_tx_throught_simple()
                    # rx_throughput_sta2 = throught.get_rx_throught_simple()
                    tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    # rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '1':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta1 = throught.get_tx_throught_simple()
                    # rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta2 = throught.get_tx_throught_simple()
                    # rx_throughput_sta2 = throught.get_rx_throught_simple()
                    tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    # rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta1 = throught.get_tx_throught_simple()
                    # rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    tx_throughput_sta2 = throught.get_tx_throught_simple()
                    # rx_throughput_sta2 = throught.get_rx_throught_simple()
                    tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    # rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    tx_tp_wirte(str(tx_throughput))
                    # rx_tp_write(str(rx_throughput))
            if TEST_UL == 1:
                if DUT_IPERF_EX == '0' and STA_IPERF_EX == '0':
                    server_ip = DUT_IP
                    client_ip = STA_IP
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput = throught.get_tx_throught_simple()
                    rx_throughput = throught.get_rx_throught_simple()
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '1':
                    server_ip = DUT_IP
                    client_ip = STA_IPERF_IP1
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput = throught.get_tx_throught_simple()
                    rx_throughput = throught.get_rx_throught_simple()
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '0' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta1 = throught.get_tx_throught_simple()
                    rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IP) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta2 = throught.get_tx_throught_simple()
                    rx_throughput_sta2 = throught.get_rx_throught_simple()
                    # tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '0':
                    server_ip = DUT_IPERF_IP1
                    client_ip = STA_IP
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput = throught.get_tx_throught_simple()
                    rx_throughput = throught.get_rx_throught_simple()
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '1':
                    server_ip = DUT_IPERF_IP1
                    client_ip = STA_IPERF_IP1
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(server_ip) + '_' + str(client_ip) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput = throught.get_tx_throught_simple()
                    rx_throughput = throught.get_rx_throught_simple()
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '1' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta1 = throught.get_tx_throught_simple()
                    rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta2 = throught.get_tx_throught_simple()
                    rx_throughput_sta2 = throught.get_rx_throught_simple()
                    # tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '0':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IP) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IP) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta1 = throught.get_tx_throught_simple()
                    rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IP) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IP) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta2 = throught.get_tx_throught_simple()
                    rx_throughput_sta2 = throught.get_rx_throught_simple()
                    # tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '1':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta1 = throught.get_tx_throught_simple()
                    rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta2 = throught.get_tx_throught_simple()
                    rx_throughput_sta2 = throught.get_rx_throught_simple()
                    # tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))
                elif DUT_IPERF_EX == '2' and STA_IPERF_EX == '2':
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP1) + '_' + str(STA_IPERF_IP1) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta1 = throught.get_tx_throught_simple()
                    rx_throughput_sta1 = throught.get_rx_throught_simple()
                    rx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Rx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP2) + '.txt'
                    tx = RADIO + '_' + str(CHANNEL) + '_' + str(i) + '_' + str(x) + '_Tx_' + str(DUT_IPERF_IP2) + '_' + str(STA_IPERF_IP2) + '.txt'
                    throught = Throught(rx, tx)
                    # tx_throughput_sta2 = throught.get_tx_throught_simple()
                    rx_throughput_sta2 = throught.get_rx_throught_simple()
                    # tx_throughput = float(tx_throughput_sta1) + float(tx_throughput_sta2)
                    rx_throughput = float(rx_throughput_sta1) + float(rx_throughput_sta2)
                    # tx_tp_wirte(str(tx_throughput))
                    rx_tp_write(str(rx_throughput))

    att.set_default()
    time.sleep(5)

def end():
    win32api.MessageBox(0,"TEST DONE",'RVR',win32con.MB_OK)
    
    

if __name__ == "__main__":
    try:
        create_result_folder()
    except Exception as err:
        logger.error('CREATE FILE FAIL')
    else:
        try:
            test()
        except Exception as err:
            logger.error('TEST FAIL')
            try:
                Generate_Test_Report()
            except Exception as err:
                logger.error('GENERATE REPORT FAIL, PLEASE MANUAL')
            else:
                logger.info('TEST DONE')
        else:
            try:
                Generate_Test_Report()
            except Exception as err:
                logger.error('GENERATE REPORT FAIL, PLEASE MANUAL')
            else:
                end()
                logger.info('TEST DONE')
