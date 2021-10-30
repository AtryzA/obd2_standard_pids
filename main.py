import multiprocessing
from gui import gui
from obd2 import OBD2
import config

def main():
    ui = gui()
    values = multiprocessing.Array('d', range(config.VALID_LEN))
    for index in range(config.VALID_LEN):
        values[index] = 0
    process = multiprocessing.Process(target=ui.start, args=[values])
    try:
        process.start()
        obd = OBD2()
        while True:
            data = obd.sequenceData()
            for index, element in enumerate(data):
                values[index] = element
    finally:
        obd.cleanup()

if __name__ == "__main__":
    main()
