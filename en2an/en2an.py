import re
from typing import Union
from collections import Counter

from . import utils
from .an2en import An2En


class En2An(object):
    def __init__(self) -> None:
        self.conf = utils.get_default_conf()
        self.all_nums = list(self.conf["number_unit"].keys())
        self.ones_nums = "|".join(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])
        self.ten_nums = "|".join(["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                                  "seventeen", "eighteen", "nineteen"])
        self.tens_nums = "|".join(["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"])
        self.all_units = "|".join(self.conf["unit_low"])
        self.ae = An2En()

    def en2an(self, inputs: str = None, mode: str = "strict") -> int:
        if inputs is not None:
            # 检查转换模式是否有效
            if mode not in ["strict", "normal", "smart"]:
                raise ValueError("mode 仅支持 strict normal smart 三种！")

            # 检查输入数据是否有效
            sign, inputs, data_type = self.check_input_data_is_valid(inputs, mode)

            if data_type == "integer":
                # 不包含小数的输入
                output = self.integer_convert(inputs)
            elif data_type == "decimal":
                point_index = inputs.index("point")
                integer_data = inputs[:point_index]
                decimal_data = inputs[point_index+1:]
                output = self.integer_convert(integer_data) + self.decimal_convert(decimal_data)
            elif data_type == "all_num":
                output = self.direct_convert(inputs)
            else:
                raise ValueError(f"输入格式错误：{inputs}！")
        else:
            raise ValueError("输入数据为空！")

        return sign * output

    def check_input_data_is_valid(self, input_check_data, mode):
        # 以空格切分，并转化成小写
        check_data = []
        for data in input_check_data.split(" "):
            low_data = data.lower()
            if "-" in low_data:
                check_data.extend(low_data.split("-"))
            else:
                check_data.append(low_data)

        # 正负号
        sign = 1

        if mode == "strict":
            strict_check_key = self.all_nums + ["minus", "and", "point"]
            for data in check_data:
                if data not in strict_check_key:
                    raise ValueError(f"当前为{mode}模式，输入的数据不在转化范围内：{data}！")

            # 确定正负号
            if check_data[0] == "minus":
                check_data = check_data[1:]
                sign = -1

        elif mode == "normal":
            normal_check_key = self.all_nums + ["minus", "negative", "and", "point", "a", ",", "，"]
            for data in check_data:
                if data not in normal_check_key:
                    raise ValueError(f"当前为{mode}模式，输入的数据不在转化范围内：{data}！")

            # 确定正负号
            if check_data[0] in ["minus", "negative"]:
                check_data = check_data[1:]
                sign = -1

        elif mode == "smart":
            smart_check_key = self.all_nums + ["minus", "and", "a", "point", ",", "，"] + [str(num) for num in range(10)]
            for data in check_data:
                if data not in smart_check_key:
                    result = re.search(r"\d+", data)
                    if result:
                        if result.group() == data:
                            break

                    raise ValueError(f"当前为{mode}模式，输入的数据不在转化范围内：{data}！")

            # 确定正负号
            if check_data[0] in ["minus", "negative"]:
                check_data = check_data[1:]
                sign = -1

            def an2en_sub(matched):
                return self.ae.an2en(matched.group()).replace("-", " ")
            check_data = re.sub(r"\d+", an2en_sub, " ".join(check_data)).split(" ")
            mode = "normal"

        if "point" in check_data:
            point_number = Counter(check_data)["point"]
            if point_number == 1:
                point_index = check_data.index("point")
                integer_data = check_data[:point_index - 1]
                decimal_data = check_data[point_index:]
            else:
                raise ValueError("数据中包含不止一个 point！")
        else:
            integer_data = check_data
            decimal_data = None

        # 整数部分检查
        twenty_to_hundred_list = []
        for tens in self.tens_nums.split("|"):
            for ones in self.ones_nums.split("|"):
                twenty_to_hundred_list.append(tens+ones)
        twenty_to_hundred = "|".join(twenty_to_hundred_list)
        under_hundred = f"{twenty_to_hundred}|{self.tens_nums}|{self.ten_nums}|{self.ones_nums}|zero"
        compile_group = f"(({self.ones_nums})hundred)?(and)?({under_hundred})?"
        ptn_normal = re.compile(f"({compile_group}({self.all_units}))*({compile_group})?")
        check_str_data = "".join(integer_data)
        re_normal = ptn_normal.search(check_str_data)

        if re_normal:
            if re_normal.group() != check_str_data:
                if mode == "strict":
                    raise ValueError(f"不符合格式的数据：{integer_data}")
                elif mode == "normal":
                    # 纯数字情况
                    ptn_all_num = re.compile(f"({self.ones_nums})+")
                    re_all_num = ptn_all_num.search(check_str_data)
                    if re_all_num:
                        if re_all_num.group() != check_str_data:
                            raise ValueError(f"不符合格式的数据：{check_data}")
                        else:
                            return sign, check_data, "all_num"
                else:
                    raise ValueError(f"不符合格式的数据：{integer_data}")
            else:
                if decimal_data:
                    return sign, check_data, "decimal"
                else:
                    if check_data[-1] == "point":
                        if mode == "strict":
                            raise ValueError(f"不符合格式的数据：{check_data}")
                        elif mode == "normal":
                            return sign, check_data, "decimal"
                    else:
                        return sign, check_data, "integer"
        else:
            if mode == "strict":
                raise ValueError(f"不符合格式的数据：{integer_data}")
            elif mode == "normal":
                if decimal_data:
                    return sign, check_data, "decimal"
                else:
                    raise ValueError(f"不符合格式的数据：{integer_data}")
            else:
                raise ValueError(f"不符合格式的数据：{integer_data}")

    def integer_convert(self, integer_data: list) -> int:
        unit = 1
        temp_num = 0
        temp_unit = 1
        output_integer = 0
        # 核心
        for index, en_num in enumerate(reversed(integer_data)):
            num = self.conf["number_unit"].get(en_num)
            # and 转化后是 None 应该去除
            if num is not None:
                if num % 1000 == 0 and num != 0:
                    output_integer += temp_num * unit
                    unit = num
                    temp_num = 0
                else:
                    if num < unit or unit == 1:
                        if num == 100:
                            temp_unit = num
                        else:
                            temp_num += int(num) * temp_unit
                            temp_unit = 1

        output_integer += temp_num * unit
        return output_integer

    def decimal_convert(self, decimal_data: list) -> float:
        len_decimal_data = len(decimal_data)

        if len_decimal_data > 15:
            print("warning: 小数部分长度为{}，超过15位有效精度长度，将自动截取前15位！".format(
                len_decimal_data))
            decimal_data = decimal_data[:15]
            len_decimal_data = 15

        output_decimal = 0
        for index in range(len(decimal_data) - 1, -1, -1):
            unit_key = self.conf["number_unit"].get(decimal_data[index])
            output_decimal += unit_key * 10 ** -(index + 1)

        # 处理精度溢出问题
        output_decimal = round(output_decimal, len_decimal_data)
        return output_decimal

    def direct_convert(self, data: list) -> Union[int, float]:
        output_data = 0
        if "point" in data:
            point_index = data.index("point")
            for index_integer in range(point_index - 1, -1, -1):
                unit_key = self.conf["number_unit"].get(data[index_integer])
                output_data += unit_key * 10 ** (point_index - index_integer - 1)

            for index_decimal in range(len(data) - 1, point_index, -1):
                unit_key = self.conf["number_unit"].get(data[index_decimal])
                output_data += unit_key * 10 ** -(index_decimal - point_index)

            # 处理精度溢出问题
            output_data = round(output_data, len(data) - point_index)
        else:
            for index in range(len(data) - 1, -1, -1):
                unit_key = self.conf["number_unit"].get(data[index])
                output_data += unit_key * 10 ** (len(data) - index - 1)

        return output_data
