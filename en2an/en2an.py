from collections import Counter

from . import utils


class En2An(object):
    def __init__(self) -> None:
        self.conf = utils.get_default_conf()
        self.all_nums = list(self.conf["number_unit"].keys())

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
                output = 0
            elif data_type == "all_num":
                output = 0
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
            normal_check_key = self.all_nums + ["minus", "and", "point", "a", ",", "，"]
            for data in check_data:
                if data not in normal_check_key:
                    raise ValueError(f"当前为{mode}模式，输入的数据不在转化范围内：{data}！")

            # 确定正负号
            if check_data[0] in ["minus", "negative"]:
                check_data = check_data[1:]
                sign = -1

        elif mode == "smart":
            smart_check_key = self.all_nums + ["minus", "and", "a", "point", ",", "，"]
            for data in check_data:
                if data not in smart_check_key:
                    raise ValueError(f"当前为{mode}模式，输入的数据不在转化范围内：{data}！")

            # 确定正负号
            if check_data[0] in ["minus", "negative"]:
                check_data = check_data[1:]
                sign = -1

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

        return sign, check_data, "integer"

    def integer_convert(self, integer_data: list) -> int:
        output_integer = 0
        max_unit = 1
        temp_num = 0
        temp_unit = 1
        # 核心
        for index, en_num in enumerate(reversed(integer_data)):
            num = self.conf["number_unit"].get(en_num)
            # and 转化后是 None 应该去除
            if num is not None:
                if num % 1000 == 0 and num != 0:
                    unit = num
                    if unit > max_unit:
                        output_integer += temp_num * max_unit
                        max_unit = unit
                        temp_num = 0
                else:
                    if num < max_unit or max_unit == 1:
                        if num == 100:
                            temp_unit = num
                        else:
                            temp_num += int(num) * temp_unit
                            temp_unit = 1

        output_integer += temp_num * max_unit
        return output_integer
