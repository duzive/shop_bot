import decimal


def fn(number):
    num = decimal.Decimal(int(number))
    return "{0:,}".format(num).replace(",", " ")
