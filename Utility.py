import random
from datetime import datetime


day = datetime.utcnow().day
month = datetime.utcnow().month
month_dict = {1: "января", 2: "февраля", 3: "марта",
              4: "апреля", 5: "мая", 6: "июня",
              7: "июля", 8: "августа", 9: "сентября",
              10: "октября", 11: "ноября", 12: "декабря"}


def shuffle(some_list):
    random.shuffle(some_list)
    return some_list[0:3]
