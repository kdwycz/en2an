import unittest

from .an2en import An2En


class En2anTest(unittest.TestCase):
    def setUp(self) -> None:
        self.strict_data_dict = {
            0: "zero",
            1: "one",
            2: "two",
            10: "ten",
            11: "eleven",
            20: "twenty",
            21: "twenty-one",
            100: "one hundred",
            220: "two hundred and twenty",
            123: "one hundred and twenty-three",
            1000: "one thousand",
            2648: "two thousand six hundred and forty-eight",
            10000: "ten thousand",
            2250062: "two million two hundred and fifty thousand sixty-two",
            100000: "one hundred thousand",
            210000: "two hundred and ten thousand",
            202202202: "two hundred and two million two hundred and two thousand two hundred and two",
            202202202202202: "two hundred and two trillion two hundred and two billion two hundred and two million two hundred and two thousand two hundred and two",
            # 0.01: "zero point zero one",
            # -1: "minus one"
        }

        self.ae = An2En()

    def test_en2an(self) -> None:
        for strict_item in self.strict_data_dict.keys():
            self.assertEqual(self.ae.an2en(strict_item, "low"), self.strict_data_dict[strict_item])


if __name__ == '__main__':
    unittest.main()
