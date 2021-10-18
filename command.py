import config

class command:
    def __init__(self) -> None:
        pass

    def get_query_command(self, command_id) -> bytes:
        formatted_command = config.MODE + command_id + '\r'
        return formatted_command.encode()

    def valid_response(self, command_id, str_reply) -> bool:
        if str_reply in config.ERORRs:
            return True
        else:
            pid, cmd = str_reply.split()[:2]
            if int(pid) == (40 + int(config.MODE)) and cmd == command_id:
                return True
            else:
                raise Exception(f'WHY NOT VALID VALUE???: pid {pid} cmd {cmd} str_reply {str_reply}')
