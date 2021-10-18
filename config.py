from dotenv import load_dotenv

from calculation import calculation
load_dotenv()

import os
ELM_ADDRESS = os.getenv('ELM_ADDRESS')
BIND_PORT = os.getenv('BIND_PORT')
CHANNEL = os.getenv('CHANNEL')
BAUDRATE = os.getenv('BAUDRATE')
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
COMMAND_FORMULA = [
    calculation.engine_load_calc,
    calculation.engine_coolant_temp_calc,
    calculation.engine_speed_calc,
    calculation.vehicle_speed_calc,
    calculation.intake_air_temp_calc,
    # calculation.mass_air_flow_calc,
    calculation.run_time_since_engine_start_calc,
    # calculation.engine_oil_temp_calc
]
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