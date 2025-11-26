# -*- coding: utf-8 -*-
# @Time    : 2020/4/23 16:01
# @Author  : Ethan

from data.parameters import DUT_NAME, DUT_TYPE, RADIO, CHANNEL, DURATION, PAIR, SERVER_SCRIPT, CLIENT_SCRIPT, SSH_PORT, STA_SSH_PORT, DUT_IPERF_EX, STA_IPERF_EX
import os
import paramiko
import logging
from time import sleep
logger = logging.getLogger()

def server_run(host, user, pwd, port):
    ssh_server = paramiko.SSHClient()
    ssh_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if DUT_IPERF_EX != '0':
        ssh_port = 22
    else:
        ssh_port = SSH_PORT
    ssh_server.connect(hostname=host, port=ssh_port, username=user, password=pwd)
    ssh_server.timeout = 0.5
    try:
        stdin, stdout, stderr = ssh_server.exec_command('taskkill.exe /im iperf3.exe /f')
    except Exception as err:
        logger.error(err)
        logger.error('No Windows')
    else:
        result = stdout.read()
        logger.debug(result)
        logger.info('windows')
    try:
        stdin, stdout, stderr = ssh_server.exec_command('killall iperf3')
        # stdin, stdout, stderr = ssh_server.exec_command('\r\nps')
    except Exception as err:
        logger.error(err)
        logger.error('No Linux')
    else:
        result = stdout.read()
        logger.debug(result)
        logger.info('Linux')
    try:
        logger.info(f'iperf3 -s -p {port} {SERVER_SCRIPT}')
        ssh_server.exec_command('iperf3 -s -p %s %s' % (port, SERVER_SCRIPT))
        # ssh_server.exec_command('dir')
        # stdin, stdout, stderr = ssh_server.exec_command('\r\nps')
    except Exception as err:
        logger.error(err)
    # finally:
    #     ssh_server.close()

def iperf3_server_local(port):
    try:
        logger.info(f'iperf3.exe -s')
        result = os.system('start iperf3.exe -s -p %s' % port)
    except Exception as err:
        logger.error(err)
    finally:
        print(result)

def iperf3_client_localDL(server_ip, client_ip, port, att, angle):
    file_path = DUT_NAME + '_' + RADIO + '/'
    log_name = RADIO+'_'+str(CHANNEL)+'_'+str(att)+'_'+str(angle)+'_TX_'+str(server_ip)+'_'+str(client_ip)+'.txt'
    os.system('del %s' % log_name)
    try:
        logger.info(f'iperf3.exe -c {server_ip} -B {client_ip} -p {port} -O 10 -f m -V -J -t {DURATION} {PAIR} -S 0x08 -R --logfile {log_name} {CLIENT_SCRIPT}')
        os.system('iperf3.exe -c %s -B %s -p %s -f m -O 10 -V -J -t %s %s -S 0x08 %s -R --logfile %s' % (server_ip, client_ip, port, DURATION, PAIR, CLIENT_SCRIPT, log_name))
    except Exception as err:
        logger.error(err)
    else:
        retval = os.getcwd()
        # print(retval)
        os.system('move %s %s/Result/iperf3/%s' %(log_name, retval, file_path))
       
def iperf3_client_localUL(server_ip, client_ip, port, att, angle):
    file_path = DUT_NAME + '_' + RADIO + '/'
    log_name = RADIO+'_'+str(CHANNEL)+'_'+str(att)+'_'+str(angle)+'_RX_'+str(server_ip)+'_'+str(client_ip)+'.txt'
    os.system('del %s' % log_name)
    try:
        logger.info(f'iperf3.exe -c {server_ip} -B {client_ip} -p {port} -f m -V -J -t {DURATION} {PAIR} -S 0x08 --logfile {log_name} {CLIENT_SCRIPT}')
        os.system('iperf3.exe -c %s -B %s -p %s -f m -O 10 -V -J -t %s %s -S 0x08 %s --logfile %s' % (server_ip, client_ip, port, DURATION, PAIR, CLIENT_SCRIPT, log_name))
    except Exception as err:
        logger.error(err)
    else:
        retval = os.getcwd()
        # print(retval)
        os.system('move %s %s/Result/iperf3/%s' %(log_name, retval, file_path))

class iperf3_client:
    def __init__(self,host,user,pwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if STA_IPERF_EX != '0':
            c_ssh_port = 22
        else:
            c_ssh_port = STA_SSH_PORT
        try:
            self.ssh.connect(hostname=host,port=c_ssh_port,username=user,password=pwd)
        except Exception as e:
            logger.info('...Connnection fail...')
        else:
            logger.info('...Connection suceess...')
            # stdin, stdout, stderr = self.ssh.exec_command('cd user_data')
            # result = stdout.read().decode('utf-8')
            # logger.info(result)
            # try:
            #     stdin, stdout, stderr = self.ssh.exec_command('mkdir Result')
            # except Exception as err:
            #     logger.error(err)
            # else:
            #     result = stdout.read().decode('utf-8')
            #     logger.info(result)
            # try:
            #     stdin, stdout, stderr = self.ssh.exec_command('cd Result')
            # except Exception as err:
            #     logger.error(err)
            # else:
            #     result = stdout.read().decode('utf-8')
            #     logger.info(result)
            # try:
            #     stdin, stdout, stderr = self.ssh.exec_command('mkdir iperf3')
            # except Exception as err:
            #     logger.error(err)
            # else:
            #     result = stdout.read().decode('utf-8')
            #     logger.info(result)
            # try:
            #     stdin, stdout, stderr = self.ssh.exec_command('cd iperf3')
            # except Exception as err:
            #     logger.error(err)
            # else:
            #     result = stdout.read().decode('utf-8')
            #     logger.info(result)
        # try:
        #     logger.debug('SFTP')
        #     logger.debug(host+user+pwd)
        #     self.transport = paramiko.Transport(host, STA_SSH_PORT)
        #     self.transport.connect(username=user, password=pwd)
        #     self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        # except Exception as err:
        #     logger.error(err)
        # else:
        #     logger.debug('SFTP list')
        #     pt = self.sftp.listdir()
        #     logger.debug(pt)
        #     # rt = self.sftp.listdir_attr()
        #     # print(rt)

    def get_file(self,host, user, pwd, filename):
        file_path = DUT_NAME + '_' + RADIO + '/'
        retval = os.getcwd()
        localpath = retval+'/Result/iperf3/'+ file_path + filename
        try:
            self.transport = paramiko.Transport(host, STA_SSH_PORT)
            self.transport.connect(username=user, password=pwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as err:
            logger.error(err)
        else:
            pt = self.sftp.listdir()
            print(pt)
            self.sftp.get(filename, localpath)

    def iper_DL(self,server_ip, client_ip, port, att, angle):
        file_path = DUT_NAME + '_' + RADIO + '/'
        log_name = RADIO+'_'+str(CHANNEL)+'_'+str(att)+'_'+str(angle)+'_TX_'+str(server_ip)+'_'+str(client_ip)+'.txt'
        try:
            self.ssh.exec_command('rm %s' % log_name)
        except Exception as err:
            logger.error(err)
        try:
            os.system('del %s' % log_name)
        except Exception as err:
            logger.error(err)
        try:
            logger.info(f'iperf3 -c {server_ip} -B {client_ip} -p {port} -f m -V -J -t {DURATION} {PAIR} -S 0x08 -R --logfile {log_name} {CLIENT_SCRIPT}')
            self.ssh.exec_command('iperf3 -c %s -B %s -p %s -f m -O 10 -V -J -t %s %s -S 0x08 %s -R --logfile %s' % (server_ip, client_ip, port, DURATION, PAIR, CLIENT_SCRIPT, log_name))
            sleep(int(DURATION)+12)
        except Exception as err:
            logger.error(err)

        retval = os.getcwd()
        localpath = retval+'/Result/iperf3/'+ file_path + log_name
        # logger.debug('remote'+log_name)
        # logger.debug('local'+localpath)
        try:
            stdin, stdout, stderr = self.ssh.exec_command(f'cat {log_name}')
            result = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            with open(localpath,'w') as f:
                f.write(result)
        except Exception as err:
            logger.error(err)
        else:
            try:
                self.ssh.exec_command('rm %s' % log_name)
            except Exception as err:
                logger.error(err)
            try:
                os.system('del %s' % log_name)
            except Exception as err:
                logger.error(err)
            self.ssh.close()
            self.transport.close()

    def iper_UL(self, server_ip, client_ip, port, att, angle):
        file_path = DUT_NAME + '_' + RADIO + '/'
        log_name = RADIO+'_'+str(CHANNEL)+'_'+str(att)+'_'+str(angle)+'_RX_'+str(server_ip)+'_'+str(client_ip)+'.txt'
        try:
            self.ssh.exec_command('rm %s' % log_name)
        except Exception as err:
            logger.error(err)
        try:
            os.system('del %s' % log_name)
        except Exception as err:
            logger.error(err)
        try:
            logger.info(f'iperf3 -c {server_ip} -B {client_ip} -p {port} -f m -V -J -t {DURATION} {PAIR} -S 0x08 --logfile {log_name} {CLIENT_SCRIPT}')
            self.ssh.exec_command('iperf3 -c %s -B %s -p %s -f m -O 10 -V -J -t %s %s -S 0x08 %s --logfile %s' % (server_ip, client_ip, port, DURATION, PAIR, CLIENT_SCRIPT, log_name))
            sleep(int(DURATION)+12)
        except Exception as err:
            logger.error(err)
        else:
            retval = os.getcwd()
            localpath = retval+'/Result/iperf3/'+ file_path+log_name
            try:
                stdin, stdout, stderr = self.ssh.exec_command(f'cat {log_name}')
                result = stdout.read().decode('utf-8')
                err = stderr.read().decode('utf-8')
                with open(localpath,'w') as f:
                    f.write(result)
            except Exception as err:
                logger.error(err)
            else:
                try:
                    self.ssh.exec_command('rm %s' % log_name)
                except Exception as err:
                    logger.error(err)
                try:
                    os.system('del %s' % log_name)
                except Exception as err:
                    logger.error(err)
                self.ssh.close()
                self.transport.close()

    def iper_S(self):
        try:
            self.ssh.exec_command('iperf3 -s')
        except Exception as err:
            logger.error(err)


if __name__ == "__main__":
    server_run('192.168.1.179','nsb','Nokia#1234', '5201')
    iperf3_client_localDL('192.168.1.179','192.168.1.80','5201','1','0')
    #tp = iperf3_client('192.168.1.1', 'root', 'adminadmin')
    #tp.iper_DL('192.168.1.2','5201','10','0')
    # tp.iper_UL('192.168.1.15','5201','10','0')
    # tp.iper_rx('192.168.1.200','10','0')
    # tp.iper_S()
    # iperf3_server_local('5201')
    # tp = iperf3_client('192.168.1.2', 'root', 'nsb@1234')
    # tp.iper_DL('192.168.12.15','5201','10','0')

    # server_run('192.168.10.1','root','adminadmin12', '5201')
    # # iperf3_client_localDL('192.168.1.201','5201','1','0')
    # tp = iperf3_client('192.168.10.2', 'root', 'nsb@1234')
    # tp.iper_DL('192.168.10.1','5201','10','0')
    # tp.get_file('192.168.1.2','root','nsb@1234','2G_6_0_0_RX.txt')



# import sys
# # import matplotlib.pyplot as plt
# import numpy as np
# import time
# import threading
# # from matplotlib import animation
# import iperf3

# # colors = ["red",
# #         "green",
# #         "blue",
# #         "rosybrown",
# #         "black"]

# # markers = ["x",
# #         "o",
# #         "v",
# #         "s",
# #         "*",
# #         ]

# # tp_pair = []
# # pair_idx = []
# # pair_cnt = 0

# # filter_str = "Mbps"
# # fig = plt.figure(figsize=(18, 8), facecolor="white")
# # plt.grid(True)
# # plt.ion()

# # class tp_item(object):
# #     idx = 0
# #     ts = 0.0
# #     mb = 0.0
# #     bw = 0
# #     def tp_init(self, line):
# #         line = line.strip()
# #         line = line.split()
# #         self.idx = int(line[1].replace("]", ""))
# #         self.ts = float(line[2].split("-")[1])
# #         self.mb = float(line[4])
# #         self.bw = float(line[6])
# #         if self.idx not in pair_idx:
# #             pair_idx.append(self.idx)
# #         update_tp(self.idx, self.ts, self.bw)

# # def __init__(self, line):
# #         self.tp_init(line)

# # def update_tp(idx, ts, bw):
# #     i = pair_idx.index(idx)
# #     tp_pair[i][0] = tp_pair[i][1]
# #     tp_pair[i][1] = ts
# #     tp_pair[i][2] = tp_pair[i][3]
# #     tp_pair[i][3] = bw

# # def dump_tp_item(i):
# #     print("id: %d, ts: %f, MBytes: %f, BW: %f"%(
# #         i.idx, i.ts, i.mb, i.bw))

# # def tp_graph(f):
# #     cur_base = 0.0
# #     prev_base = 0.0
# #     while True:
# #         try:
# #             while cur_base == prev_base:
# #                 l = f.readline()
# #                 if (filter_str in l) and ("SUM" not in l):
# #                     item = tp_item(l)
# #                     dump_tp_item(item)
# #                     if (cur_base == 0.0 and prev_base == 0.0):
# #                         prev_base = cur_base = item.ts
# #                     else:
# #                         prev_base = cur_base
# #                         cur_base = item.ts
# #             for i in range(len(pair_idx)):
# #                 plt.plot([tp_pair[i][0], tp_pair[i][1]], [tp_pair[i][2], tp_pair[i][3]],
# #                         color=colors[i], marker=markers[i])
# #                 plt.text(tp_pair[i][1], tp_pair[i][3], tp_pair[i][3], ha="center", va="bottom", fontsize=15)
# #             plt.pause(1)
# #             prev_base = cur_base
# #         except Exception as err:
# #             print(err)

# # def gen_tp_pair(num):
# #     for i in range(num):
# #         tp_pair.append([])
# #         for j in range(4):
# #             tp_pair[i].append(0)

# # if __name__ == '__main__':
# #     pair_num = 1
# #     if len(sys.argv) < 3:
# #         print("Usage: iperf_tp.py <file path> <flow num>")
# #         exit(-1)
# #     pair_num = int(sys.argv[2])
# #     pair_cnt = pair_num
# #     gen_tp_pair(pair_num)
# #     print(tp_pair)
# #     f = open(sys.argv[1], mode='r')
# #     print("Open: %s"%(sys.argv[1]))
# #     tp_graph(f)
# #     f.close()


# print('hello')
# client = iperf3.Client()
# # client.duration = 1
# # client.bind_address = '10.0.0.1'
# # client.server_hostame = '10.10.10.10'
# # client.port = 6969
# # client.blksize = 1234
# # client.num_streams = 10
# # client.zerocopy = True
# # client.verbose = False
# # client.reverse = True
# # client.run()
