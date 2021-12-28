import csv
import datetime
import array
import sys
import subprocess
import serial
from serial.serialutil import SerialException
import re
from command import command
from calculation import calculation
import config

def debug(str):
    print(f'----{str}----')

class OBD2:
    def __init__(self) -> None:
        self.clc = calculation()
        self.socket = None
        self.process_listen = None
        try:
            self.setup()
        except Exception as e:
            print(e)
            self.cleanup()
            sys.exit()
        try:
            logpath = "output/"
            filename = "log_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".csv"
            self.fullpath = logpath + filename
            init_info = list(config.PIDs.keys())
            with open(self.fullpath, "w", newline="") as logfile:
                writer = csv.writer(logfile)
                writer.writerow(init_info)
        except Exception as e:
            print(e)
            self.cleanup()
            sys.exit()

    def setup(self) -> None:
        debug('Set UP')
        self.bindingBluetooth()
        self.createSocket(config.BAUDRATE)
        self.elm_setting()

    def elm_setting(self) -> None:
        debug('ELM Setting')
        self.socket.write(b'ATZ\r')
        self.waitCommand()
        self.socket.write(b'ATL1\r')
        self.waitCommand()
        self.socket.write(b'ATE0\r')

    def cleanup(self) -> None:
        debug('Clean UP')
        try:
            self.socket.close()
        except Exception as e:
            print(e)
        self.process_listen.kill()
        subprocess.run(['sudo', 'rfcomm', 'release', str(config.BIND_PORT)])

    def bindingBluetooth(self) -> None:
        debug('Binding')
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'])
        subprocess.run(['sudo', 'rfcomm', 'bind', str(config.BIND_PORT), str(config.ELM_ADDRESS)])
        self.process_listen = subprocess.Popen(['rfcomm', 'listen', str(config.BIND_PORT), str(config.CHANNEL), '&'])

    def createSocket(self, baudrate) -> None:
        debug('CreateSocket')
        try:
            self.socket = serial.Serial(f'/dev/rfcomm{config.BIND_PORT}', baudrate)
        except SerialException:
            raise Exception('Connection Failed')

    def commandQuery(self, query, command_name) -> bytes:
        debug(f'{command_name} Query')
        self.socket.write(query)
        reply = self.socket.readline()
        format_reply = re.sub('\s?\r\n$', '', reply.decode('ascii'))
        return format_reply

    def sequenceData(self) -> array:
        values = []
        for pname, cmd in config.PIDs.items():
            str_reply = None
            try:
                str_reply = self.commandQuery(command.get_query_command(self, cmd), pname)
                if command.valid_response(self, cmd, str_reply):
                    value = self.clc.calc_value(pname, str_reply)
                    print(f'{pname} : {value} {config.UNITs[pname]}')
                    values.append(value)
                else:
                    self.error(pname)
            except Exception as e:
                print(e)
                print(f'not valid: {str_reply}')
            self.waitCommand()
        return values

    def waitCommand(self):
        # debug('Wait')
        reply = ''
        while reply != b'>':
            reply = self.socket.read()
            # print(f'garbage: {reply}')
        return True

    def error(self, cmd) -> None:
        debug('Query Error')
        print(f'The value by {cmd} was not returned')
