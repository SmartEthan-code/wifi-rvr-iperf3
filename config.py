# -*- coding:utf-8 -*-

"""for config file"""

__author__ = 'Ethan'


# from data.parameters import DEBUG_LOG
import configparser
import time
import logging


# create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# # create a handler 
# log_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
# file_handler = logging.FileHandler('./log/log_'+log_time+'.txt', mode='w')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# logger.addHandler(file_handler)

# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# logger.addHandler(console_handler)


config_file = "./config/config.ini"


class Config:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Dut_name_get(self):
        apname = self.conf.get("dut_config", "name")
        logger.info(f'dut name is:{apname}')
        return apname

    def Dut_type_get(self):
        aptype = self.conf.get("dut_config", "type")
        logger.info(f'dut type is:{aptype}')
        return aptype

    def Dutip_get(self):
        dutip = self.conf.get("dut_config", "ip")
        logger.info("dut ip is     : {0}".format(dutip))
        return dutip

    def Username_get(self):
        username = self.conf.get("dut_config", "username")
        logger.info("user name is     : {0}".format(username))
        return username

    def Password_get(self):
        password = self.conf.get("dut_config", "password")
        logger.info("password is     : {0}".format(password))
        return password

    def SSID_get(self):
        ssid = self.conf.get("dut_config", "ssid")
        logger.info("SSID is     : {0}".format(ssid))
        return ssid

    def Radio_get(self):
        radio = self.conf.get("dut_config", "radio")
        logger.info("radio is     : {0}".format(radio))
        return radio

    def Channel_get(self):
        channel = self.conf.get("dut_config", "channel")
        logger.info("channel is     : {0}".format(channel))
        return channel

    def SSH_enable_get(self):
        ssh_enable = self.conf.get("dut_config", "ssh_enable")
        logger.info("SSH Enable   : {}".format(ssh_enable))
        return ssh_enable

    def SSH_port_get(self):
        ssh_port = self.conf.get("dut_config", "ssh_port")
        logger.info("SSH Port is   : {}".format(ssh_port))
        return ssh_port

    def serial_enable_get(self):
        serial_enable = self.conf.get("dut_config", "serial_enable")
        logger.info("Serial Enable   : {}".format(serial_enable))
        return serial_enable

    def COM_get(self):
        ap_com = self.conf.get("dut_config", "com")
        logger.info("AP COM is     : {0}".format(ap_com))
        return ap_com

    def Baudrate_get(self):
        ap_baudrate = self.conf.get("dut_config", "baudrate")
        logger.info("AP Baudrate is     : {0}".format(ap_baudrate))
        return ap_baudrate

    def telnet_enable_get(self):
        telnet_enable = self.conf.get("dut_config", "telnet_enable")
        logger.info("Telnet Enable   : {}".format(telnet_enable))
        return telnet_enable

    def telnet_port_get(self):
        telnet_port = self.conf.get("dut_config", "telnet_port")
        logger.info("Telnet Port is   : {}".format(telnet_port))
        return telnet_port
    
    def adb_enable_get(self):
        adb_enable = self.conf.get("dut_config", "adb_enable")
        logger.info("ADB Enable   : {}".format(adb_enable))
        return adb_enable

    def dut_internal_get(self):
        dut_internal = self.conf.get("dut_config", "iperf_internal")
        logger.info("Dut iperf internal is     : {0}".format(dut_internal))
        return dut_internal

    def dut_external_get(self):
        dut_external = self.conf.get("dut_config", "iperf_external")
        logger.info("Dut iperf external is     : {0}".format(dut_external))
        return dut_external

    def dut1_ip_get(self):
        dut1_ip = self.conf.get("dut_config", "iperf_IP1")
        logger.info("Dut iperf IP1 is     : {0}".format(dut1_ip))
        return dut1_ip

    def dut2_ip_get(self):
        dut2_ip = self.conf.get("dut_config", "iperf_IP2")
        logger.info("Dut iperf IP2 is     : {0}".format(dut2_ip))
        return dut2_ip

    def dut1_username_get(self):
        dut1_username = self.conf.get("dut_config", "ex_1_username")
        logger.info("Dut ex1 username is     : {0}".format(dut1_username))
        return dut1_username

    def dut1_password_get(self):
        dut1_password = self.conf.get("dut_config", "ex_1_password")
        logger.info("Dut ex1 password is     : {0}".format(dut1_password))
        return dut1_password    

    def dut2_username_get(self):
        dut2_username = self.conf.get("dut_config", "ex_2_username")
        logger.info("Dut ex2 username is     : {0}".format(dut2_username))
        return dut2_username

    def dut2_password_get(self):
        dut2_password = self.conf.get("dut_config", "ex_2_password")
        logger.info("Dut ex2 password is     : {0}".format(dut2_password))
        return dut2_password  

    def Sta_type_get(self):
        sta_type = self.conf.get("sta_config", "type")
        logger.info("sta type is     : {0}".format(sta_type))
        return sta_type

    def Adapter_get(self):
        adapter = self.conf.get("sta_config", "adapter_name")
        logger.info("adapter_name is     : {0}".format(adapter))
        return adapter

    def Sta_ip(self):
        sta_ip = self.conf.get("sta_config", "ip")
        logger.info("sta ip is     : {0}".format(sta_ip))
        return sta_ip

    def Sta_username(self):
        sta_username = self.conf.get("sta_config", "username")
        logger.info("sta username is     : {0}".format(sta_username))
        return sta_username

    def Sta_password(self):
        sta_password = self.conf.get("sta_config", "password")
        logger.info("sta password is     : {0}".format(sta_password))
        return sta_password

    def Sta_sshenable_get(self):
        sta_ssh_enable = self.conf.get("sta_config", "ssh_enable")
        logger.info("STA SSH Enable   : {}".format(sta_ssh_enable))
        return sta_ssh_enable
    
    def Sta_sshport_get(self):
        sta_ssh_port = self.conf.get("sta_config", "ssh_port")
        logger.info("STA ssh port is     : {0}".format(sta_ssh_port))
        return sta_ssh_port

    def Sta_serialenable_get(self):
        sta_serial_enable = self.conf.get("sta_config", "serial_enable")
        logger.info("STA Serial Enable   : {}".format(sta_serial_enable))
        return sta_serial_enable

    def Sta_COM_get(self):
        sta_com = self.conf.get("sta_config", "com")
        logger.info("STA COM is     : {0}".format(sta_com))
        return sta_com

    def Sta_Baudrate_get(self):
        sta_baudrate = self.conf.get("sta_config", "baudrate")
        logger.info("AP Baudrate is     : {0}".format(sta_baudrate))
        return sta_baudrate

    def Sta_telnetenable_get(self):
        sta_telnet_enable = self.conf.get("sta_config", "telnet_enable")
        logger.info("Telnet Enable   : {}".format(sta_telnet_enable))
        return sta_telnet_enable

    def Sta_telnetport_get(self):
        sta_telnet_port = self.conf.get("sta_config", "telnet_port")
        logger.info("Telnet Port is   : {}".format(sta_telnet_port))
        return sta_telnet_port
    
    def Sta_adbenable_get(self):
        sta_adb_enable = self.conf.get("sta_config", "adb_enable")
        logger.info("ADB Enable   : {}".format(sta_adb_enable))
        return sta_adb_enable

    # def Sta_switchip_get(self):
    #     sta_switch_ip = self.conf.get("sta_config", "switch_ip")
    #     logger.info("sta switch ip is     : {0}".format(sta_switch_ip))
    #     return sta_switch_ip

    # def Sta_switchport_get(self):
    #     sta_switch_port = self.conf.get("sta_config", "switch_port")
    #     logger.info("sta switch port is     : {0}".format(sta_switch_port))
    #     return sta_switch_port

    def sta_internal_get(self):
        sta_internal = self.conf.get("sta_config", "iperf_internal")
        logger.info("Sta iperf internal is     : {0}".format(sta_internal))
        return sta_internal

    def sta_external_get(self):
        sta_external = self.conf.get("sta_config", "iperf_external")
        logger.info("Sta iperf external is     : {0}".format(sta_external))
        return sta_external

    def sta1_ip_get(self):
        sta1_ip = self.conf.get("sta_config", "iperf_IP1")
        logger.info("Sta iperf IP1 is     : {0}".format(sta1_ip))
        return sta1_ip

    def sta2_ip_get(self):
        sta2_ip = self.conf.get("sta_config", "iperf_IP2")
        logger.info("Sta iperf IP2 is     : {0}".format(sta2_ip))
        return sta2_ip

    def sta1_username_get(self):
        sta1_username = self.conf.get("sta_config", "ex_username")
        logger.info("Sta ex1 username is     : {0}".format(sta1_username))
        return sta1_username

    def sta1_password_get(self):
        sta1_password = self.conf.get("sta_config", "ex_password")
        logger.info("Sta ex1 password is     : {0}".format(sta1_password))
        return sta1_password    

    def sta2_username_get(self):
        sta2_username = self.conf.get("sta_config", "ex_2_username")
        logger.info("Sta ex2 username is     : {0}".format(sta2_username))
        return sta2_username

    def sta2_password_get(self):
        sta2_password = self.conf.get("sta_config", "ex_2_password")
        logger.info("Sta ex2 password is     : {0}".format(sta2_password))
        return sta2_password  

    def Atten_start_get(self):
        atten_start = self.conf.get("atten_config", "atten_start")
        logger.info("atten start    : {0}".format(atten_start))
        return atten_start

    def Atten_end_get(self):
        atten_end = self.conf.get("atten_config", "atten_end")
        logger.info("atten end     : {0}".format(atten_end))
        return atten_end

    def Atten_step_get(self):
        atten_step = self.conf.get("atten_config", "atten_step")
        logger.info("atten step is     : {0}".format(atten_step))
        return atten_step

    def External_loss_get(self):
        external_loss = self.conf.get("atten_config", "external_loss")
        logger.info("external loss is     : {0}".format(external_loss))
        return external_loss

    def Atten_1_ip_get(self):
        att_1_ip = self.conf.get("atten_config", "ip")
        logger.info("atten ip is     : {0}".format(att_1_ip))
        return att_1_ip

    def Atten_2_ip_get(self):
        att_2_ip = self.conf.get("atten_config", "att_2_ip")
        logger.info("atten 2 ip is     : {0}".format(att_2_ip))
        return att_2_ip

    def Atten_3_ip_get(self):
        att_3_ip = self.conf.get("atten_config", "att_3_ip")
        logger.info("atten 3 ip is     : {0}".format(att_3_ip))
        return att_3_ip

    def Atten_4_ip_get(self):
        att_4_ip = self.conf.get("atten_config", "att_4_ip")
        logger.info("atten 4 ip is     : {0}".format(att_4_ip))
        return att_4_ip

    def Atten_5_ip_get(self):
        att_5_ip = self.conf.get("atten_config", "att_5_ip")
        logger.info("atten 5 ip is     : {0}".format(att_5_ip))
        return att_5_ip

    def Atten_6_ip_get(self):
        att_6_ip = self.conf.get("atten_config", "att_6_ip")
        logger.info("atten 6 ip is     : {0}".format(att_6_ip))
        return att_6_ip

    def Atten_7_ip_get(self):
        att_7_ip = self.conf.get("atten_config", "att_7_ip")
        logger.info("atten 7 ip is     : {0}".format(att_7_ip))
        return att_7_ip

    def Atten_8_ip_get(self):
        att_8_ip = self.conf.get("atten_config", "att_8_ip")
        logger.info("atten 8 ip is     : {0}".format(att_8_ip))
        return att_8_ip

    def Port1_get(self):
        iperf_port1 = self.conf.get("iperf_config", "port1")
        logger.info("Iperf port1 is    : {0}".format(iperf_port1))
        return iperf_port1

    def Port2_get(self):
        iperf_port2 = self.conf.get("iperf_config", "port2")
        logger.info("Iperf port2 is    : {0}".format(iperf_port2))
        return iperf_port2

    def Pair_number_get(self):
        pair = self.conf.get("iperf_config", "pair")
        logger.info("pari number is    : {0}".format(pair))
        return pair

    def Duration_get(self):
        duration = self.conf.get("iperf_config", "duration")
        logger.info("duration time is    : {0}".format(duration))
        return duration

    def Server_script_get(self):
        server_script = self.conf.get("iperf_config", "server_script")
        logger.info("server_script time is    : {0}".format(server_script))
        return server_script

    def Client_script_get(self):
        client_script = self.conf.get("iperf_config", "client_script")
        logger.info("server_script time is    : {0}".format(client_script))
        return client_script

    def Curr_att_get(self):
        curr_att = self.conf.get("atten_config", "current_atten")
        logger.info("current attention is    : {0}".format(curr_att))
        return curr_att

    def angle_num_get(self):
        angle_num = self.conf.get("swivel_table_config", "angle_num")
        logger.info("Degree is     : {0}".format(angle_num))
        return angle_num

    def current_angle_get(self):
        current_angle = self.conf.get("swivel_table_config", "current_angle")
        logger.info("Current_angle is     : {0}".format(current_angle))
        return current_angle

    def table_ip_get(self):
        table_ip = self.conf.get("swivel_table_config", "ip")
        logger.info("Table IP is     : {0}".format(table_ip))
        return table_ip

    def table_com_get(self):
        table_com = self.conf.get("swivel_table_config", "com")
        logger.info("Table COM is     : {0}".format(table_com))
        return table_com

    def Run_type_get(self):
        run_type = self.conf.get("test_config", "test_type")
        logger.info("Run type is    : {0}".format(run_type))
        return run_type

    def Test_dl_get(self):
        test_dl = self.conf.get("test_config", "test_dl")
        logger.info("Test dl is     : {0}".format(test_dl))
        return test_dl

    def Test_ul_get(self):
        test_ul = self.conf.get("test_config", "test_ul")
        logger.info("Test ul is     : {0}".format(test_ul))
        return test_ul

    def Run_time_get(self):
        run_time = self.conf.get("test_config", "test_time")
        logger.info("Run time is    : {0}".format(run_time))
        return run_time

    def Debug_log_get(self):
        debug_log = self.conf.get("test_config", "debug_log")
        logger.info("Debug log is    : {0}".format(debug_log))
        return debug_log

# AP配置参数写入
class Dut_config(object):
    def __init__(self, duttype, dutip, username, password, radio, channel):
        self.duttype = duttype
        self.dutip = dutip
        self.username = username
        self.password = password
        self.radio = radio
        self.channel = channel
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def dut_config_set(self):
        self.conf.set("dut_config", "duttype", str(self.duttype))
        self.conf.set("dut_config", "dutip", str(self.dutip))
        self.conf.set("dut_config", "username", str(self.username))
        self.conf.set("dut_config", "password", str(self.password))
        self.conf.set("dut_config", "radio", str(self.radio))
        self.conf.set("dut_config", "channel", str(self.channel))
        self.conf.write(open(config_file, "w"))


# 衰减配置写入
class Atten_config(object):
    def __init__(self, start, end, step, loss, num):
        self.atten_start = start
        self.atten_end = end
        self.atten_step = step
        self.line_loss = loss
        self.atten_num = num
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Atten_config_set(self):
        self.conf.set("atten_config", "atten_start", str(self.atten_start))
        self.conf.set("atten_config", "atten_end", str(self.atten_end))
        self.conf.set("atten_config", "atten_step", str(self.atten_step))
        self.conf.set("atten_config", "line_loss", str(self.line_loss))
        self.conf.set("atten_config", "atten_num", str(self.atten_num))
        self.conf.write(open(config_file, "w"))


# chariot配置写入
class iperf_config(object):
    def __init__(self, pcip, staip, duration, pairnumber):
        self.pcip = pcip
        self.staip = staip
        self.duration = duration
        self.pairnumber = pairnumber
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def chariot_set(self):
        self.conf.set("iperf_config", "pc_ip", str(self.pcip))
        self.conf.set("iperf_config", "sta_ip", str(self.staip))
        self.conf.set("iperf_config", "duration", str(self.duration))
        self.conf.set("iperf_config", "pairnumber", str(self.pairnumber))
        self.conf.write(open(config_file, "w"))


# 写配置，以便生成以当前衰减和角度命名的报告
class Con_current_atten:
    def __init__(self, atten):
        self.atten = atten
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def read_atten(self):
        current_atten = self.conf.get("atten_config", "current_atten")
        logger.info("now the attention is   : {0}".format(current_atten))
        return current_atten

    def write_atten(self):
        self.conf.set("atten_config", "current_atten", str(self.atten))
        self.conf.write(open(config_file, "w"))


# 写配置，以便生成以当前衰减和角度命名的报告
class Con_current_angle:
    def __init__(self, angle):
        self.angle = angle
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def read_current_angle(self):
        #print('111', self.angle)
        angle = self.conf.get("swivel_table_config", "current_angle")
        #print('222', angle)
        logger.info("now the angle is   : {0}".format(angle))
        return angle

    def write_angle(self):
        self.conf.set("swivel_table_config", "current_angle", str(self.angle))
        self.conf.write(open(config_file, "w"))


# 圆盘电机角度配置写入
class Swivel_table_config(object):
    def __init__(self, angle):
        self.angle = angle
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def swivel_table_type_set(self):
        self.conf.set("swivel_table_config", "angle", str(self.angle))
        self.conf.write(open(config_file, "w"))


# 终端类型配置写入
class Sta_config(object):
    def __init__(self, statype):
        self.sta_type = statype
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Sta_type_set(self):
        self.conf.set("sta_config", "sta_type", str(self.sta_type))
        self.conf.write(open(config_file, "w"))


# 测试类型写入
class Run_type_config(object):
    def __init__(self, runtype):
        self.run_type = runtype
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Run_type_set(self):
        self.conf.set("test_config", "test_type", str(self.run_type))
        self.conf.write(open(config_file, "w"))

class Run_time_config(object):
    def __init__(self, runtime):
        self.run_time = runtime
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def Run_time_read(self):
        current_time = self.conf.get("test_config", "current_time")
        logger.info("now the time is   : {0}".format(current_time))
        return current_time

    def Run_time_set(self):
        self.conf.set("test_config", "current_time", str(self.run_time))
        self.conf.write(open(config_file, "w"))


conf = Config()


if __name__ == "__main__":
    #pass##
    ##dut_conf=Dut_config("WF-1821","192.168.188.251","admin","password","2","6")
    ##dut_conf.dut_config_set()
    ##chariot=iperf_config("192.168.1.10","192.168.1.20",90,8,10)
    ##chariot.chariot_set()
    get = Config()
    ip = get.Atten_1_ip_get()
    print(ip)
    print(get)
    for i in {10, 20}:
        x = 20
        att = Con_current_atten(20)
        value = att.read_atten()
        print(value)

        att.write_atten()
        value = att.read_atten()
        print(value)

    for i in {10, 20}:
        x = 20
        angle = Con_current_angle(90)
        value = angle.read_current_angle()
        print(value)

        angle.write_angle()
        value = angle.read_current_angle()
        print(value)



    #atten.Atten_config_set()
    #staconfig=Sta_config("WF-2821")
    #staconfig.Sta_type_set()"""
