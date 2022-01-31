import multiprocessing
import threading
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
        obd_thread = threading.Thread(target=obd.start, args=(values,))
        obd_thread.daemon = True
        obd_thread.start()
        ui.start(values)
    except:
        obd.cleanup()
        ui.cleanup()

if __name__ == "__main__":
    main()
