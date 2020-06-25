import unittest

from .en2an import En2An


class En2anTest(unittest.TestCase):
    def setUp(self) -> None:
        self.strict_data_dict = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "ten": 10,
            "eleven": 11,
            "twenty-one": 21,
            "one hundred": 100,
            "two hundred and twenty": 220,
            "one hundred and twenty-three": 123,
            "two thousand six hundred and forty-eight": 2648,
            "two million two hundred and fifty thousand sixty-two": 2250062,
            "two hundred and two million two hundred and two thousand two hundred and two": 202202202,
            "two hundred and two trillion two hundred and two billion two hundred and two million two hundred and two thousand two hundred and two": 202202202202202,
            "zero point zero one": 0.01,
            "zero point zero one zero one zero one zero one zero one zero one zero one zero one": 0.01010101010101,
            "minus one": -1
        }

        self.normal_data_dict = {
            "one two three four": 1234,
            "one two three point four": 123.4,
        }

        self.normal_data_dict.update(self.strict_data_dict)

        self.smart_data_dict = {
            "10 million": 10000000,
            "10 million 1000": 10001000,
            "one hundred 23": 123
        }
        self.smart_data_dict.update(self.normal_data_dict)

        self.ea = En2An()

    def test_en2an(self) -> None:
        for strict_item in self.strict_data_dict.keys():
            self.assertEqual(self.ea.en2an(strict_item, "strict"), self.strict_data_dict[strict_item])

        for normal_item in self.normal_data_dict.keys():
            self.assertEqual(self.ea.en2an(normal_item, "normal"), self.normal_data_dict[normal_item])

        for smart_item in self.smart_data_dict.keys():
            self.assertEqual(self.ea.en2an(smart_item, "smart"), self.smart_data_dict[smart_item])


if __name__ == '__main__':
    unittest.main()
