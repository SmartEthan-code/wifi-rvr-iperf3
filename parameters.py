__author__ = 'DVTRF'

from config import conf


# ap
DUT_NAME = str(conf.Dut_name_get()).strip()
DUT_TYPE = str(conf.Dut_type_get()).strip()
DUT_IP = str(conf.Dutip_get()).strip()
DUT_USERNAME = str(conf.Username_get()).strip()
DUT_PASSWORD = str(conf.Password_get()).strip()
SSID = str(conf.SSID_get()).strip()
RADIO = str(conf.Radio_get()).strip()
CHANNEL = int(conf.Channel_get().strip())
SSH_EN = int(conf.SSH_enable_get().strip())
SSH_PORT = int(conf.SSH_port_get().strip())
SERIAL_EN = int(conf.serial_enable_get().strip())
SERIAL_COM = str(conf.COM_get()).strip()
SERIAL_BAUDRATE = str(conf.Baudrate_get()).strip()
TELNET_EN = int(conf.telnet_enable_get().strip())
TELNET_PORT = int(conf.telnet_port_get().strip())
ADB_EN = int(conf.adb_enable_get().strip())
# DUT_IPERF_IN = str(conf.dut_internal_get()).strip()
DUT_IPERF_EX = str(conf.dut_external_get()).strip()
DUT_IPERF_IP1 = str(conf.dut1_ip_get()).strip()
DUT_IPERF_IP2 = str(conf.dut2_ip_get()).strip()
DUT_EX1_USERNAME = str(conf.dut1_username_get()).strip()
DUT_EX1_PASSWORD = str(conf.dut1_password_get()).strip()
DUT_EX2_USERNAME = str(conf.dut2_username_get()).strip()
DUT_EX2_PASSWORD = str(conf.dut2_password_get()).strip()

# station parameters
STA_TYPE = str(conf.Sta_type_get()).strip()
ADAPTER = str(conf.Adapter_get()).strip()
STA_IP = str(conf.Sta_ip()).strip()
STA_USERNAME = str(conf.Sta_username()).strip()
STA_PASSWORD = str(conf.Sta_password()).strip()
STA_SSH_EN = int(conf.Sta_sshenable_get().strip())
STA_SSH_PORT = int(conf.Sta_sshport_get().strip())
STA_SERIAL_EN = int(conf.Sta_serialenable_get().strip())
STA_SERIAL_COM = str(conf.Sta_COM_get()).strip()
STA_SERIAL_BAUDRATE = str(conf.Sta_Baudrate_get()).strip()
STA_TELNET_EN = int(conf.Sta_telnetenable_get().strip())
STA_TELNET_PORT = int(conf.Sta_telnetport_get().strip())
STA_ADB_EN = int(conf.Sta_adbenable_get().strip())
# STA_SWITCHIP = str(conf.Sta_switchip_get()).strip()
# STA_SWITCHPORT = str(conf.Sta_switchport_get()).strip()
# STA_IPERF_IN = str(conf.sta_internal_get()).strip()
STA_IPERF_EX = str(conf.sta_external_get()).strip()
STA_IPERF_IP1 = str(conf.sta1_ip_get()).strip()
STA_IPERF_IP2 = str(conf.sta2_ip_get()).strip()
STA_EX_USERNAME = str(conf.sta1_username_get()).strip()
STA_EX_PASSWORD = str(conf.sta1_password_get()).strip()
# STA_EX2_USERNAME = str(conf.sta2_username_get()).strip()
# STA_EX2_PASSWORD = str(conf.sta2_password_get()).strip()

# att
ATTEN_START = int(conf.Atten_start_get())
ATTEN_END = int(conf.Atten_end_get())
ATTEN_STEP = int(conf.Atten_step_get())
LINE_LOSS = int(conf.External_loss_get())
CURRENT_ATT = int(conf.Curr_att_get())
ATTEN_1_IP = str(conf.Atten_1_ip_get())
# ATTEN_2_IP = str(conf.Atten_2_ip_get())
ATTENUATE_LIST = []
ATT = ATTEN_START
while ATT <= ATTEN_END:
    ATTENUATE_LIST.append(ATT)
    ATT = ATT + ATTEN_STEP

# iperf
IPERF_PORT1 = int(conf.Port1_get().strip())
IPERF_PORT2 = int(conf.Port2_get().strip())
PAIR = str(conf.Pair_number_get().strip())
DURATION = int(conf.Duration_get().strip())
SERVER_SCRIPT = str(conf.Server_script_get().strip())
CLIENT_SCRIPT = str(conf.Client_script_get().strip())

# turntable
ANGLE_NUM = int(conf.angle_num_get())
angle_setup = 360.0 / float(ANGLE_NUM)
angle = 0
ANGLE_LIST = []
while angle < 360.0:
    ANGLE_LIST.append(angle)
    angle += angle_setup
TABLE_IP = str(conf.table_ip_get()).strip()
TABLE_COM = str(conf.table_com_get()).strip()

# TESTTYPE
RUN_TPYE = int(conf.Run_type_get())
TEST_DL = int(conf.Test_dl_get())
TEST_UL = int(conf.Test_ul_get())
RUN_TIME = str(conf.Run_time_get().strip())
DEBUG_LOG = str(conf.Debug_log_get()).strip()
