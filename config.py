from dotenv import load_dotenv
load_dotenv()

import os
ELM_ADDRESS = os.getenv('ELM_ADDRESS')
BIND_PORT = os.getenv('BIND_PORT')
CHANNEL = os.getenv('CHANNEL')
BAUDRATE = os.getenv('BAUDRATE')