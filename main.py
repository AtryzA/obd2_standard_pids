from obd2 import OBD2
from command import PIDs, UNITs, command
from calculation import calculation

def main():
    obd = OBD2()
    cmd = command()
    calc = calculation()
    try:
        while True:
            for pname, comd in PIDs.items():
                try:
                    str_reply = obd.commandQuery(cmd.get_query(comd), pname)
                    if cmd.valid_response(comd, str_reply):
                        value = calc.calc_value(pname, str_reply)
                        print(f'{pname} : {value} {UNITs[pname]}')
                    else:
                        obd.error(pname)
                except:
                    print(f'not valid: {str_reply}')
                obd.waitCommand()
    finally:
        obd.cleanup()

if __name__ == "__main__":
    main()
