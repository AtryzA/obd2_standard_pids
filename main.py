import multiprocessing
from gui import gui
from obd2 import OBD2

def main():
    ui = gui()
    process = multiprocessing.Process(target=ui.start)
    obd = OBD2()
    try:
        process.start()
        while True:
            values = obd.sequenceData()
            print(values)
    finally:
        obd.cleanup()

if __name__ == "__main__":
    main()
