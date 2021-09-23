import array
from command import PIDs

class calculation:
    def __init__(self) -> None:
        pass

    def calc_value(self, command_name, str_reply) -> int:
        command_formula = [
            self.engine_load_calc,
            self.engine_coolant_temp_calc,
            self.engine_speed_calc,
            self.vehicle_speed_calc,
            self.intake_air_temp_calc,
            # self.mass_air_flow_calc,
            self.run_time_since_engine_start_calc,
            # self.engine_oil_temp_calc
        ]
        command_map = dict.fromkeys(PIDs, None)
        for index, pid in enumerate(PIDs):
            command_map[pid] = command_formula[index]
        try:
            value = command_map[command_name](str_reply)
            return value
        except:
            raise Exception(f"Can't calc {command_name}: (str_reply){str_reply}")

    def byte_2_int(self, str_reply) -> array:
        byte2array = str_reply.split()[2:]
        value_array = []
        for value_byte in byte2array:
            value_hex = bytes.fromhex(value_byte)
            value_array.append(int.from_bytes(value_hex, 'big'))
        if len(value_array) == 1:
            return value_array.pop()
        return value_array

    def engine_load_calc(self, value) -> int:
        A = self.byte_2_int(value)
        calc_value = 100 / 255 * int(A)
        return calc_value

    def engine_coolant_temp_calc(self, value) -> int:
        A = self.byte_2_int(value)
        calc_value = int(A) - 40
        return calc_value

    def engine_speed_calc(self, value) -> int:
        A, B = self.byte_2_int(value)
        calc_value = (256 * int(A) + int(B)) /4
        return calc_value

    def vehicle_speed_calc(self, value) -> int:
        A = self.byte_2_int(value)
        calc_value = int(A)
        return calc_value

    def intake_air_temp_calc(self, value) -> int:
        A = self.byte_2_int(value)
        calc_value = int(A) - 40
        return calc_value

    def mass_air_flow_calc(self, value) -> int:
        A, B = self.byte_2_int(value)
        calc_value = (256 * int(A) + int(B)) / 100
        return calc_value

    def run_time_since_engine_start_calc(self, value) -> int:
        A, B = self.byte_2_int(value)
        calc_value = 256 * int(A) + int(B)
        return calc_value

    def engine_oil_temp_calc(self, value) -> int:
        A = self.byte_2_int(value)
        calc_value = int(A) - 40
        return calc_value