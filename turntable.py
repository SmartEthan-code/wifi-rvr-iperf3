# -*- coding: utf-8 -*-
# @Time    : 2020/09/03 10:00
# @Author  : Ethan

"""for turn_table setting"""

import telnetlib
import re
import time
import logging
logger = logging.getLogger()

class Turntable:
    def __init__(self, ip):
        self.tn = telnetlib.Telnet(ip, 50000)
        self.tn.set_debuglevel(1)

    def login(self, username, password):
        if username:
            self.tn.read_until(b'UserName:')
            self.tn.write(username.encode('ascii') + b'\r\n')
            if password:
                self.tn.read_until(b'Password:')
                self.tn.write(password.encode('ascii') + b'\r\n')
            else:
                logger.info('No password')
        else:
            logger.info('No user')
    def close(self):
        # print(self.tn)
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def status(self):
        self.tn.write('gcp\r\n'.encode('ascii'))
        time.sleep(1)
        command_result = self.tn.read_very_eager()
        print(command_result)
        stat = re.findall(b'(.+)\r\n', command_result)[0].decode('utf-8')
        print(stat)
        return stat

    def set_angle(self, angle):
        angle = float(angle)*10
        # self.tn.read_until('>'.encode('ascii'))
        self.tn.write('rt'.encode('ascii')+' %d\r\n'.encode('ascii') % angle)
        # stat = self.status()
        # while float(stat) != angle:
        #     stat = self.status()
        # self.tn.write('att\r\n'.encode('ascii'))
        # command_result = self.tn.read_all()
        # logger.debug(command_result)
            # command_result = re.search(
            #     b'([1-9]\d*\.?\d*)|(0\.\d*[0-9])\r\n', command_result)
            # logger.debug(command_result)
            # status_value = '1'
            # if status_value == '1':
            #     logger.info('Attenuation Settings Successful! Value=%s' %
            #                 set_value)
            # else:
            #     logger.error('Attenuation Settings Fail')

    def set_default(self):
        self.tn.write('rt'.encode('ascii')+' 0\r\n'.encode('ascii'))
        time.sleep(15)
        # stat = self.status()
        # while float(stat) != 0.0:
        #     stat = self.status()


if __name__ == '__main__':
    value = 180
    table = Turntable('10.1.0.18')
    # table.status()
    table.set_default()
    time.sleep(20)
    table.set_angle(value)
    table.close()








# import snap7

# client = snap7.client.Client()

# client.connect('192.168.0.1', 0, 1)

# client.disconnect()