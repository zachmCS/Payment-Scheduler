from datetime import date
from datetime import timedelta
import holidays


def main():
    ## Say a payment is due one month (30 days) after February 9th, 2023.
    originalDate = date(2023, 2, 9)
    dueDate = originalDate + timedelta(days=30)  # dueDate = 2023-03-11, which is a Saturday.
    print("The payment is due on " + str(
        nextBusDay(dueDate)) + ".")  # The next business day is 3-13 (Monday), so the payment is due on 3-13.


def nextBusDay(date):  # after calculating what exact day a payment should fall on, this function will
    # either return that date if it is a business day, or the next business day if it is a weekend or holiday
    us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
    while date.weekday() in holidays.WEEKEND or date in us_holidays:
        date += timedelta(days=1)
    return date


def prevBusDay(date):  # after calculating what exact day a payment should fall on, this function will
    # either return that date if it is a business day, or the previous business day if it is a weekend or holiday
    us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
    while date.weekday() in holidays.WEEKEND or date in us_holidays:
        date -= timedelta(days=1)
    return date

def prevBusDayModded(date):  # after calculating what exact day a payment should fall on, this function will
    # either return that date if it is a business day, or the previous business day if it is a weekend or holiday stopping
    # at the last first day of the month
    us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
    while date.weekday() in holidays.WEEKEND or date in us_holidays:
        if (date - timedelta(days=1)).month == date.month:
            date -= timedelta(days=1)
        else:
            nextBusDayModded(date)

    return date



def nextBusDayModed(date):  # after calculating what exact day a payment should fall on, this function will
    # either return that date if it is a business day, or the next business day if it is a weekend or holiday stopping
    # at the last day of the month
    us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
    while date.weekday() in holidays.WEEKEND or date in us_holidays:
        if (date + timedelta(days=1)).month == date.month:
            date += timedelta(days=1)
        else:
            prevBusDayModded(date)

    return date


main()