#!/user/bin/env python
# encoding: utf-8
# @time      : 2020/4/27 13:28

__author__ = 'Ethan'

"""for switch setting"""

from time import sleep
from data.parameters import RUN_TPYE
import telnetlib
import re
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理

# # 第二步，创建一个handler，用于写入日志文件
# file_handler = logging.FileHandler('./log/log.txt', mode='w')
# file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 创建该handler的formatter
# file_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# # 添加handler到logger中
# logger.addHandler(file_handler)

# # 第三步，创建一个handler，用于输出到控制台
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
# # 创建该handler的formatter
# console_handler.setFormatter(
#         logging.Formatter(
#                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')
#         )
# logger.addHandler(console_handler)


class Switch:
    def __init__(self, ip):
        self.tn = telnetlib.Telnet(ip,50000)
        self.tn.set_debuglevel(1)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def set_switch_runtype(self):
        if RUN_TPYE == 1:
            logger.info('Conductive')
            self.tn.write(b'SW 1 0 2 1 3 0 4 1 5 0 6 1 7 0 8 1\n')
            command_result = self.tn.read_until(b'\d+\;\n\r', timeout=1)
            logger.debug(command_result)
            logger.info(f'Switch Setting Successful! \r\n{command_result.decode()}')
        else:
            logger.info('OTA')
            self.tn.write(b'SW 1 1 2 0 3 1 4 0 5 1 6 0 7 1 8 0\n')
            command_result = self.tn.read_until(b'\d+\;\n\r', timeout=1)
            logger.debug(command_result)
            logger.info(f'Switch Setting Successful! \r\n{command_result.decode()}')

    def set_default(self):
        self.tn.write(b'SW' + b'\n')


if __name__ == '__main__':
    swt = Switch('10.1.0.12')
    # swt.set_default()
    #swt.set_switch_sta('4')
    swt.set_switch_runtype()
    swt.close()
