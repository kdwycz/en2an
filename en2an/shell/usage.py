from time import ctime

from en2an.version import VERSION


def run():
    cur_time = ctime()
    text = f"""
    # en2an: Convert English Numerals To Arabic Numerals
    
    Version {VERSION} ({cur_time} +0800)
    """
    print(text)
