from typing import Union

from . import utils


class An2En(object):
    def __init__(self) -> None:
        self.conf = utils.get_default_conf()

    def an2en(self, inputs: Union[str, int] = None, mode: str = "low") -> str:
        if inputs is not None:
            sign = ""
            if mode not in ["low", "up", "usd"]:
                raise ValueError("mode 仅支持 low up usd 三种！")

            # 将数字转化为字符串
            if not isinstance(inputs, str):
                inputs = self._convert_number_to_string(inputs)

            # 将全角数字和符号转化为半角，增加对全角数字和全角符号的支持
            inputs = self.__full_to_half(inputs)

            # 检查数据是否有效
            self._check_inputs_is_valid(inputs)

            # 判断正负
            if inputs[0] == "-":
                inputs = inputs[1:]
                sign = "minus "

            # 切割整数部分和小数部分
            split_result = inputs.split(".")
            len_split_result = len(split_result)
            if len_split_result == 1:
                # 不包含小数的输入
                integer_data = split_result[0]
                output = self._integer_convert(integer_data, mode)
            else:
                raise ValueError(f"输入格式错误：{inputs}！")
        else:
            raise ValueError(f"输入数据为空！")

        return sign + output

    @staticmethod
    def __full_to_half(ustring: str) -> str:
        # 全角转半角
        r = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            # 全角空格直接转换
            if inside_code == 12288:
                inside_code = 32
            # 全角字符（除空格）根据关系转化
            elif 65281 <= inside_code <= 65374:
                inside_code -= 65248
            else:
                pass
            r += chr(inside_code)
        return r

    @staticmethod
    def _check_inputs_is_valid(check_data: str) -> None:
        # 检查输入数据是否在规定的字典中
        all_check_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
        for data in check_data:
            if data not in all_check_keys:
                raise ValueError(f"输入的数据不在转化范围内：{data}！")

    @staticmethod
    def _convert_number_to_string(number_data: int) -> str:
        # python 会自动把 0.00005 转化成 5e-05，因此 str(0.00005) != "0.00005"
        string_data = str(number_data)
        if "e" in string_data:
            string_data_list = string_data.split("e")
            string_key = string_data_list[0]
            string_value = string_data_list[1]
            if string_value[0] == "-":
                string_data = "0." + "0" * (int(string_value[1:]) - 1) + string_key
            else:
                string_data = string_key + "0" * int(string_value)

        return string_data

    def _integer_convert(self, integer_data: str, mode: str) -> str:
        numeral_list = self.conf[f"number_low"]
        unit_ten_list = self.conf[f"unit_ten_low"]
        unit_list = self.conf[f"unit_low"]
        max_len = self.conf["max_len"]

        # 去除前面的 0，比如 007 => 7
        integer_data = str(int(integer_data))

        data_len = len(integer_data)
        if data_len > max_len:
            raise ValueError(f"超出数据范围，最长支持 {max_len} 位")

        output_en = ""
        en = ""
        is_ten_unit = False
        is_zero = False
        for i, d in enumerate(integer_data):
            data = int(d)
            n = (data_len - (i + 1)) % 3
            m = (data_len - (i + 1)) // 3 - 1

            if n == 2:
                if data != 0:
                    en = numeral_list[data] + " hundred"
            elif n == 1:
                if data == 1:
                    is_ten_unit = True
                elif data in range(2, 10):
                    if en != "":
                        en = en + " and " + unit_ten_list[data]
                    else:
                        en = unit_ten_list[data]
                else:
                    # 0 跳过
                    is_zero = True
            elif n == 0:
                if is_ten_unit:
                    if data != 0:
                        if en != "":
                            en = en + " and " + numeral_list[10+data]
                        else:
                            # 11-19
                            en = numeral_list[10+data]
                    else:
                        # 10
                        en = numeral_list[10+data]
                    is_ten_unit = False
                else:
                    if data != 0:
                        if en != "":
                            if is_zero:
                                en = en + " and " + numeral_list[data]
                                is_zero = False
                            else:
                                en = en + "-" + numeral_list[data]
                        else:
                            en = numeral_list[data]
                    else:
                        # 0
                        if m < 0 and output_en == "" and en == "":
                            en = numeral_list[data]

                if m < 0:
                    output_en = output_en + en
                else:
                    output_en = output_en + en + " " + unit_list[m] + " "

                en = ""

        if output_en[-1] == " ":
            output_en = output_en[:-1]

        if mode == "up":
            output_en = output_en.upper()
        elif mode == "usd":
            output_en = f"SAY US DOLLARS {output_en.upper()} ONLY"

        return output_en
