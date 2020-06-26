import torbjorn as tbn

from .an2en import An2En
from .en2an import En2An

ae = An2En()
ea = En2An()

an = 123456789012345
en = "one hundred and twenty-three trillion four hundred and fifty-six billion seven hundred and eighty-nine million twelve thousand three hundred and forty-five"


@tbn.run_time
def run_en2an_ten_thousand_times() -> None:
    for _ in range(10000):
        result = ea.en2an(en)
        assert result == an


@tbn.run_time
def run_an2en_ten_thousand_times() -> None:
    for _ in range(10000):
        result = ae.an2en(an)
        assert result == en


if __name__ == '__main__':
    run_en2an_ten_thousand_times()
    run_an2en_ten_thousand_times()
