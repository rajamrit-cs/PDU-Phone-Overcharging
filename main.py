#!/usr/bin/env python3
"""
Date: 28-12-2022
By: Amrit Raj @ Candela Technologies Pvt. ltd.
Note: Please ensure that PDU is powered on
    Command line to be used as
    python pdu_automation.py --host 192.168.200.49 --user admin --password pass1234 --action on/off/cycle --port all/specific_port_number
    Eg 1: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action off --port 1
    Eg 2: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action off --port 1,2,3,4
    Eg 3: python pdu_v3.py --host 192.168.200.49 --user admin --password pass1234 --action cycle --port all
"""
import os
import time
import argparse
from typing import Sequence
from typing import Optional

try:
    import dlipower
except:
    print('Please wait we are installing DLI Power module for you!!!')
    os.system('pip install dlipower')


class PDUAutomate:
    def __init__(self, hostname, user, password):
        self.port = None
        self.hostname = hostname
        self.user = user
        self.password = password
        self.power_switch = None
        try:
            self.power_switch = dlipower.PowerSwitch(hostname=self.hostname, userid=self.user, password=self.password)
        except:
            print('PDU device is Off, please connect it and try after sometime!!!')
            exit(0)

    def start(self, action, port):
        if action == "on":
            self.switch_on(port)
        elif action == "off":
            self.switch_off(port)
        elif action == "cycle":
            self.switch_off(port)
            self.switch_on(port)
        else:
            print("[ERROR] Wrong input")

    def switch_on(self, port):
        self.port = port
        if self.port != 'all':
            try:
                port = str(self.port).split(",")
                print(port)
                for i in port:
                    self.power_switch[int(i) - 1].state = "ON"
            except:
                self.power_switch[int(self.port) - 1].state = "ON"
        else:
            for outlet in self.power_switch:
                outlet.state = 'ON'

    def switch_off(self, port):
        self.port = port
        if self.port != 'all':
            try:
                port = str(self.port).split(",")
                print(port)
                for i in port:
                    self.power_switch[int(i) - 1].state = "OFF"
            except:
                self.power_switch[int(self.port) - 1].state = "OFF"
        else:
            for outlet in self.power_switch:
                outlet.state = 'OFF'

    def print_status(self):
        print(self.power_switch)


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Please provide host name eg: 192.168.200.65')
    parser.add_argument('--username', help='Please provide username eg: admin')
    parser.add_argument('--password', help='Please provide password eg: 1234')
    parser.add_argument('--action', help='Switches all Outlets in ON Mode eg: --on or --off')
    parser.add_argument('--port', help='Please provide port name eg: --port 1,2,3,4')
    args = parser.parse_args(argv)
    dic = vars(args)

    obj = PDUAutomate(dic['host'], dic['username'], dic['password'])
    obj.start(dic['action'], dic['port'])


if __name__ == '__main__':
    main()


# python main.py --host 192.168.200.50 --user admin --password Candela@123 --current on/off --port 2 --on_time 2hrs
# --off_time 5hrs
# from here for 2 hours it should charge and for 5hrs it should be in off condition
