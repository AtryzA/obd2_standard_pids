MODE = '01'
PIDs = {
    "ENGINE_LOAD" : '04',
    "ENGINE_COOLANT_TEMP" : '05',
    "ENGINE_SPEED" : '0C',
    "VEHICLE_SPEED" : '0D',
    "INTAKE_AIR_TEMP" : '0F',
    # "MASS_AIR_FLOW" : '10',
    "RUN_TIME_SINCE_ENGINE_START" : '1F',
    # "ENGINE_OIL_TEMP" : '5C',
}
UNITs = {
    "ENGINE_LOAD" : '%',
    "ENGINE_COOLANT_TEMP" : '°C',
    "ENGINE_SPEED" : 'RPM',
    "VEHICLE_SPEED" : 'km/h',
    "INTAKE_AIR_TEMP" : '°C',
    # "MASS_AIR_FLOW" : 'grams/sec',
    "RUN_TIME_SINCE_ENGINE_START" : 'seconds',
    # "ENGINE_OIL_TEMP" : '°C',
}
ERORRs = [
    'UNABLE TO CONNECT',
    'BUS INIT... ERROR',
    '?',
    'NO DATA',
    'STOPPED',
    'ERROR'
]

class command:
    def __init__(self) -> None:
        pass

    def valid_response(self, command_id, str_reply) -> bool:
        if str_reply in ERORRs:
            return True
        else:
            pid, cmd = str_reply.split()[:2]
            if int(pid) == (40 + int(MODE)) and cmd == command_id:
                return True
            else:
                raise Exception(f'WHY NOT VALID VALUE???: pid {pid} cmd {cmd} str_reply {str_reply}')

    def get_query(self, command_id) -> bytes:
        formatted_command = MODE + command_id + '\r'
        return formatted_command.encode()
