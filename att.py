# -*- coding: utf-8 -*-
# @Time    : 2020/4/23 15:15
# @Author  : Ethan

"""for attenuate setting"""

import telnetlib
import re
import time
import logging
logger = logging.getLogger()

class Attenuate:
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

    def set_att(self, attenuate_value):
        for pathb in range(1,9):
            # self.tn.read_until('>'.encode('ascii'))
            self.tn.write(b'ATT %d %d\n' % (pathb, int(attenuate_value)))
            time.sleep(1)
        # for pathb in range(1,9):
        #     # self.tn.read_until('>'.encode('ascii'))
        #     self.tn.write(b'ATT %d %d\n' % (pathb, int(attenuate_value)))
        self.tn.write(b'ATT\n')
        command_result = self.tn.read_until(b'\;\n\r', timeout=1)
        logger.debug(command_result)
        logger.info(f'Att Setting Successful! \r\n{command_result.decode()}')
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

    # def set_default(self):
    #     self.tn.write('ATT\r\n'.encode('ascii'))
    #     for patha in range(1,9):
    #         # self.tn.read_until('>'.encode('ascii'))
    #         self.tn.write('ATT'.encode('ascii')+' %d 0\r\n'.encode('ascii') % patha)

    def set_default(self):
       self.tn.write(b'ATT 1 0 2 0 3 0 4 0 5 0 6 0 7 0 8 0\n')
       time.sleep(3)
    


if __name__ == '__main__':
    value = 54
    att = Attenuate('192.168.1.28')
    # att.login('user 1','')
    att.set_default()
    att.set_att(value)
    att.close()
