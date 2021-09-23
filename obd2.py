import sys
import subprocess
import serial
from serial.serialutil import SerialException
import re
import config

def debug(str):
    print(f'----{str}----')

class OBD2:
    def __init__(self) -> None:
        self.socket = None
        self.process_listen = None
        try:
            self.setup()
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
        except:
            pass
        self.process_listen.kill()
        subprocess.run(['sudo', 'rfcomm', 'release', str(config.BIND_PORT)])

    def bindingBluetooth(self) -> None:
        debug('Binding')
        subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'])
        subprocess.run(['sudo', 'hcitool', 'scan', '--flush'])
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
