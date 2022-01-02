import time
import multiprocessing
from gui import gui
from obd2 import OBD2
import config

def main():
    try:
        obd = OBD2()
        ui = gui()
        values = multiprocessing.Array('d', range(config.VALID_PIDs_LEN))
        for index in range(config.VALID_PIDs_LEN):
            values[index] = 0
        obd_process = multiprocessing.Process(target=obd.start, args=[values])
        ui_process = multiprocessing.Process(target=ui.start, args=[values])
        process = [obd_process, ui_process]
        for p in process:
            p.start()
    except:
        # obd.cleanup()
        ui.cleanup()

if __name__ == "__main__":
    main()
