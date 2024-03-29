from copy import deepcopy
import datetime
from itertools import chain
from enum import Enum
from typing import Dict, Iterable, Tuple, Union, runtime_checkable
import holidays
import pandas as pd
from jdcal import gcal2jd, is_leap


class Date():
    """ of Financial Date Class"""

    def __init__(self, day: int, month: int, year: int) -> None:
        """
               Initializes a self with a day, month and a year
               :param day: day given for a self
               :param month: month given for self
               :param year: year given for self
        """
        self.day = day
        self.month = month
        self.year = year

    # returns day
    def get_day(self) -> int:
        return self.day

    # returns month
    def get_month(self) -> int:
        return self.month

    # returns year
    def get_year(self) -> int:
        return self.year

    # returns julian day
    def get_julian_day(self) -> int:
        jyear = gcal2jd(self.year, self.month, self.day)
        jyear = jyear[0] + jyear[1] + 0.5
        return jyear

    # checks if it is a leap year
    def is_leap_year(self) -> bool:
        return is_leap(self.year)

    # checks if is the given day is a business day
    def is_bus_day(self, calendar_input: "Calendar") -> bool:
        # need to get bank type from scheduler
        if not calendar_input.is_holiday(self) and not calendar_input.is_weekend(self):
            return True
        return False

    # turns the given self date info into actual date object
    def as_date(self) -> datetime:
        # print(datetime.date(self.year, self.month, self.day))
        return datetime.date(self.year, self.month, self.day)

    def __repr__(self) -> str:
        return f'DATE (Month: "{self.month}", Day: "{self.day}", Year: {self.year})'

    def __str__(self) -> str:
        return f'({self.month},{self.day},{self.year})'

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day))

    # TODO: Add implement frequency portion
    # Can add day, week, month, or year at a given unit
    # i.e. 1 day, 2 weeks, 3 months at a frequency
    # i.e. monthly. bimonthly, annually, once
    def __add__(self, other: Union[int, "Frequency", "Term"]) -> "Date":
        pass

    # TODO need to implement frequency portion
    # Can subtract day, week, month, or year at a given unit
    # i.e. 1 day, 2 weeks, 3 months at a frequency
    # i.e. monthly. bimonthly, annually, once
    def __sub__(self, other: Union[int, "Frequency", "Term"]) -> "Date":
        pass

    def __eq__(self, other: "Date") -> bool:
        if isinstance(other, self.__class__):
            return self.year == other.year and self.month == other.month and self.day == other.day
        return False

    def __gt__(self, other: "Date") -> bool:
        if isinstance(other, self.__class__):
            return self.as_date() > other.as_date()
        return False

    def __ge__(self, other: "Date") -> bool:
        if isinstance(other, self.__class__):
            return self.as_date() >= other.as_date()
        return False

    def __lt__(self, other: "Date") -> bool:
        if isinstance(other, self.__class__):
            return self.as_date() < other.as_date()
        return False

    def __le__(self, other: "Date") -> bool:
        if isinstance(other, self.__class__):
            return self.as_date() <= other.as_date()
        return False


def to_last_day(input_date):
    if input_date.month == 12:
        return input_date.replace(day=31)
    return input_date.replace(month=input_date.month + 1, day=1) - datetime.timedelta(days=1)


class BusinessDayRule():
    """ of Business Day Rule Representation"""

    # TODO: Add implement end of the month rule more directly into the code

    def __init__(self, start_date: Date, end_date: Date, rules: str, ruleSet: str,
                 country_chosen, end_of_month_rule, custom_val=1, custom_freq='') -> None:
        """
            Initializes a self with a start_date, end_date, rules for the business option
            selected, and the country chosen for the bank holidays
            :param start_date: day you start searching from
            :param end_date: day stop searching at
            :param rules: ruleset the business will pull from
            :param country_chosen: the country whose holiday we will look for bank holidays are from
        """
        self.start_date = start_date
        self.end_date = end_date
        self.rules = rules  # NOTE: This is the cadence of the payment
        self.ruleSet = ruleSet  # NOTE: This is the rule set that is used to determine the business day
        self.country_chosen = country_chosen
        self.end_of_the_month_rule = end_of_month_rule
        self.custom_val = custom_val if custom_val else 1
        self.custom_freq = custom_freq

    # updates end of the month rule
    def update_month_rule(self, rule_value: bool):
        self.end_of_the_month_rule = rule_value

    # updates payment specification
    def update_payment(self, new_payment: str):
        self.payments = new_payment


    cadence_map = {
        "Days": 1,
        "Weekly": 1,
        "Bi-Weekly": 2,
        "Monthly": 1,
        "Bi-Monthly": 2,
        "Quarterly": 3,
        "Semi-Annually": 6,
        "Annually": 12,
    }

    custom_map = {
        "Day(s)": 'Days', 
        "Week(s)": 'Weekly',
        "Month(s)": 'Monthly',
        "Year(s)": 'Annually'
    }

    def num_payments_cal(self) -> int:
        if self.rules == "Weekly":
            return (self.end_date.as_date() - self.start_date.as_date()).days // 7
        elif self.rules == "Bi-Weekly":
            return (self.end_date.as_date() - self.start_date.as_date()).days // 14
        elif self.rules == "Monthly":
            return (self.end_date.year - self.start_date.year) * 12 + (self.end_date.month - self.start_date.month)
        elif self.rules == "Bi-Monthly":
            return (self.end_date.year - self.start_date.year) * 6 + (self.end_date.month - self.start_date.month) // 2
        elif self.rules == "Quarterly":
            return (self.end_date.year - self.start_date.year) * 4 + (self.end_date.month - self.start_date.month) // 3
        elif self.rules == "Semi-Annually":
            return (self.end_date.year - self.start_date.year) * 2 + (self.end_date.month - self.start_date.month) // 6
        elif self.rules == "Annually":
            return self.end_date.year - self.start_date.year
        elif self.rules == "Custom":
            self.rules = self.custom_map[self.custom_freq]
            if self.custom_freq == 'Day(s)':
                return (self.end_date.as_date() - self.start_date.as_date()).days // self.custom_val
            elif self.custom_freq == 'Week(s)':
                return (self.end_date.as_date() - self.start_date.as_date()).days // (7 * self.custom_val)
            elif self.custom_freq == 'Month(s)':
                return (self.end_date.year - self.start_date.year) * 12 + (self.end_date.month - self.start_date.month) // self.custom_val
            elif self.custom_freq == 'Year(s)':
                return (self.end_date.year - self.start_date.year) // self.custom_val
    # after calculating what exact day a payment should fall on, this function will
    # either return that self if it is a business day, or the next business day if it is a weekend or holiday
    def calc_payment_dates(self, given_date: Date):
        returned = []
        if self.ruleSet == "Following Business Day":
            returned = self.next_bus_day(given_date)
        elif self.ruleSet == "Preceding Business Day":
            returned = self.prev_bus_day(given_date)
        elif self.ruleSet == "Modified Following Business Day":
            returned = self.next_bus_day_modded(given_date)
        elif self.ruleSet == "Modified Preceding Business Day":
            returned = self.prev_bus_day_modded(given_date)
        elif self.ruleSet == "No Adjustment":
            returned = self.no_adjustment(given_date)
        return returned

    def next_bus_day(self, given_date: Date):
        given = given_date.as_date()
        start = given
        end_start = deepcopy(given)
        payment_dates = []
        num_payments = self.num_payments_cal()
        for i in range(num_payments):
            cadence_value = BusinessDayRule.cadence_map[self.rules] * self.custom_val
            given = start + pd.DateOffset(
                days=cadence_value * (i + 1)) if "day" in self.rules.lower() else start + pd.DateOffset(
                weeks=cadence_value * (i + 1)) if "week" in self.rules.lower() else start + pd.DateOffset(
                months=cadence_value * (i + 1))
            if self.end_of_the_month_rule and (given_date.as_date() == to_last_day(given_date.as_date())):
                given = to_last_day(given)
            while given.weekday() > 4 or given in self.country_chosen:
                given += pd.DateOffset(days=1)
            # If the date does not exist in payment_dates already AND it is within our range, append it
            if given not in payment_dates and given.date() <= self.end_date.as_date():
                payment_dates.append(given)
        return payment_dates

    # after calculating what exact day a payment should fall on, this function will
    # either return that self if it is a business day, or the previous business day if it is a weekend or holiday
    def prev_bus_day(self, given_date: Date):
        given = given_date.as_date()
        start = given
        payment_dates = []
        num_payments = self.num_payments_cal()
        for i in range(num_payments):
            cadence_value = BusinessDayRule.cadence_map[self.rules] * self.custom_val
            given = start + pd.DateOffset(
                days=cadence_value * (i + 1)) if "day" in self.rules.lower() else start + pd.DateOffset(
                weeks=cadence_value * (i + 1)) if "week" in self.rules.lower() else start + pd.DateOffset(
                months=cadence_value * (i + 1))
            if self.end_of_the_month_rule and (given_date.as_date() == to_last_day(given_date.as_date())):
                given = to_last_day(given)
            while given.weekday() > 4 or given in self.country_chosen:
                given -= pd.DateOffset(days=1)
            if given not in payment_dates and given.date() <= self.end_date.as_date():
                payment_dates.append(given)
        return payment_dates

    # after calculating what exact day a payment should fall on, this function will
    # either return that self if it is a business day, or the next business day if
    # it is a weekend or holiday stopping at the last day of the month
    # Note ask about circumfiting infinte loops (or going into the next month using Marcos method)
    def next_bus_day_modded(self, given_date: Date):
        given = given_date.as_date()
        start = given
        payment_dates = []
        num_payments = self.num_payments_cal()
        for i in range(num_payments):
            cadence_value = BusinessDayRule.cadence_map[self.rules] * self.custom_val
            given = start + pd.DateOffset(
                days=cadence_value * (i + 1)) if "day" in self.rules.lower() else start + pd.DateOffset(
                weeks=cadence_value * (i + 1)) if "week" in self.rules.lower() else start + pd.DateOffset(
                months=cadence_value * (i + 1))
            if self.end_of_the_month_rule and (given_date.as_date() == to_last_day(given_date.as_date())):
                given = to_last_day(given)
            while given.weekday() > 4 or given in self.country_chosen:
                if (given + pd.DateOffset(days=1)).month == given.month:
                    given += pd.DateOffset(days=1)
                else:
                    while given.weekday() > 4 or given in self.country_chosen:
                        given -= pd.DateOffset(days=1)
            if given not in payment_dates and given.date() <= self.end_date.as_date():
                payment_dates.append(given)
        return payment_dates

    # after calculating what exact day a payment should fall on, this function will
    # either return that self if it is a business day, or the previous business day
    # if it is a weekend or holiday stopping at the first day of the month
    def prev_bus_day_modded(self, given_date: Date):
        given = given_date.as_date()
        start = given
        payment_dates = []
        num_payments = self.num_payments_cal()
        for i in range(num_payments):
            cadence_value = BusinessDayRule.cadence_map[self.rules] * self.custom_val
            given = start + pd.DateOffset(
                days=cadence_value * (i + 1)) if "day" in self.rules.lower() else start + pd.DateOffset(
                weeks=cadence_value * (i + 1)) if "week" in self.rules.lower() else start + pd.DateOffset(
                months=cadence_value * (i + 1))
            if self.end_of_the_month_rule and (given_date.as_date() == to_last_day(given_date.as_date())):
                given = to_last_day(given)
            while given.weekday() > 4 or given in self.country_chosen:
                if (given - pd.DateOffset(days=1)).month == given.month:
                    given -= pd.DateOffset(days=1)
                else:
                    while given.weekday() > 4 or given in self.country_chosen:
                        given += pd.DateOffset(days=1)
            if given not in payment_dates and given.date() <= self.end_date.as_date():
                payment_dates.append(given)
        return payment_dates
    
    def no_adjustment(self, given_date: Date):
        given = given_date.as_date()
        start = given
        payment_dates = []
        num_payments = self.num_payments_cal()
        for i in range(num_payments):
            cadence_value = BusinessDayRule.cadence_map[self.rules] * self.custom_val
            given = start + pd.DateOffset(
                days=cadence_value * (i + 1)) if "day" in self.rules.lower() else start + pd.DateOffset(
                weeks=cadence_value * (i + 1)) if "week" in self.rules.lower() else start + pd.DateOffset(
                months=cadence_value * (i + 1))
            if self.end_of_the_month_rule and (given_date.as_date() == to_last_day(given_date.as_date())):
                given = to_last_day(given)
            if given not in payment_dates and given.date() <= self.end_date.as_date():
                payment_dates.append(given)
        return payment_dates


class Frequency():
    """ of Frequency Representation"""

    name: str
    term: "Term"
    numerical: float

    @property
    def year_fraction(self) -> float:
        return self.numerical

    def __str__(self) -> str:
        return f'({self.name},{self.term},{self.numerical})'


class DayOfTheWeek(Enum):
    MON, TUE, WED, THU, FRI, SAT, SUN = range(7)


class Calendar():
    """ of Financial Calendar class"""

    def __init__(
            self,
            weekend: Iterable[DayOfTheWeek],
            holiday: Iterable[Date],
    ) -> None:
        self.weekend = weekend
        self.holiday = holiday

    def __eq__(self, other: "Calendar") -> bool:
        return self.weekend == other.weekend and self.holiday == other.holiday

    def __str__(self) -> str:
        return f'({list(self.weekend)},{list(self.holiday)})'

    def add_holiday(self, date_input: Date):
        if date_input not in self.holiday:
            chain(self.holiday, [date_input])

    def add_holidays(self, dates_input: Iterable[Date]):
        for date in dates_input:
            if date not in self.holiday:
                chain(self.holiday, [date])

    def is_weekend(self, date_input: Date) -> bool:
        if date_input not in self.weekend:
            return False
        else:
            return True

    def is_holiday(self, date_input: Date) -> bool:
        if date_input not in self.holiday:
            return False
        else:
            return True

    def is_bus_day(
            self, date_input: Date, ignore_weekend: bool, ignore_holidays: bool
    ) -> bool:
        # checks the ignored bools to return the correct check to see if it is a business day
        # if both ignore bools are false then is_holiday and is_weekend need to be checked
        # if both are true then every day is a business holiday and return will always be true
        if not ignore_weekend and not ignore_holidays:
            if self.is_holiday(date_input) or self.is_weekend(date_input):
                return False
            else:
                return True
        elif not ignore_weekend:
            if self.is_weekend(date_input):
                return False
            else:
                return True
        elif not ignore_holidays:
            if self.is_holiday(date_input):
                return False
            else:
                return True
        else:
            return True

    # TODO
    def bus_to_cal_day(
            self,
            date_input: Date,
            term_input: "Term",
            business_day_rule: BusinessDayRule,
            ignore_weekend: bool,
            ignore_holidays: bool,
    ) -> "Term":
        pass

    def business_days_between(
            self,
            start_date: Date,
            end_date: Date,
            ignore_weekend: bool,
            ignore_holidays: bool,
    ) -> int:
        dates = (start_date.as_date() + datetime.timedelta(day + 1)
                 for day in range((end_date.as_date() - start_date.as_date()).days))
        res = sum(1 for day_input in dates if self.is_bus_day(Date(day_input.day, day_input.month, day_input.year),
                                                              ignore_weekend, ignore_holidays))
        return res


class TermUnit():
    """ of Term Unit Representation"""

    name: str
    code: str

    def __str__(self) -> str:
        return f'(Name: {self.name}, Code: {self.code})'


class Term():
    """Financial Term Class"""
    quantity: int
    unit: TermUnit

    CODE_TO_TERM_MAP: Dict[str, TermUnit]

    def __init__(
            self, quantity: int, unit: Union[TermUnit, str], lenient: bool = False
    ) -> None:
        """

        """
        self.quantity = quantity
        self.unit = unit
        self.lenient = lenient

    # TODO what is this?
    @classmethod
    def from_str(cls, string: str, lenient: bool = False) -> "Term":
        pass

    def __str__(self) -> str:
        return f'(Quantity: {self.quantity}, Term: {self.unit}, Leniency: {self.lenient})'

    def __float__(self) -> float:
        return float(self.quantity)

    def __repr__(self) -> str:
        return f'(Quantity: {self.quantity}, ' \
               f'Term: {self.unit} -> TermUnit: (Name: {self.unit.name}, Code: {self.unit.code}),' \
               f' Leniency: {self.lenient})'

    def __hash__(self) -> int:
        return hash((self.quantity, self.unit.name, self.unit.code, self.lenient))

    # TODO Same problem with Date where two units can have different weights
    # Currently, only works if two units are the same (conversion maybe needed)
    def __add__(self, other: "Term") -> "Term":
        if isinstance(other, self.__class__):
            if self.unit == other.unit and self.lenient == other.lenient:
                sum_term = Term(self.quantity + other.quantity, self.unit, self.lenient)
                return sum_term

    def __sub__(self, other: "Term") -> "Term":
        if self.unit == other.unit and self.lenient == other.lenient:
            sub_term = Term(self.quantity - other.quantity, self.unit, self.lenient)
            return sub_term

    def __mul__(self, other: int) -> "Term":
        mul_term = Term(self.quantity * other, self.unit, self.lenient)
        return mul_term

    def __floordiv__(self, other: int) -> "Term":
        fdiv_term = Term(self.quantity // other, self.unit, self.lenient)
        return fdiv_term

    def __mod__(self, other: int) -> "Term":
        mod_term = Term(self.quantity % other, self.unit, self.lenient)
        return mod_term

    def __truediv__(self, other: int) -> "Term":
        div_term = Term(self.quantity * other, self.unit, self.lenient)
        return div_term

    def __eq__(self, other: "Term") -> bool:
        if isinstance(other, self.__class__):
            return self.quantity == other.quantity and self.unit == other.unit and self.lenient == other.lenient

    # TODO Same problem as Data where units can change
    # Currently, only works if two units are the same (conversion maybe needed)
    def __gt__(self, other: "Term") -> bool:
        if isinstance(other, self.__class__):
            if self.unit == other.unit and self.lenient == other.lenient:
                return self.quantity > other.quantity
        return False

    def __ge__(self, other: "Term") -> bool:
        if isinstance(other, self.__class__):
            if self.unit == other.unit and self.lenient == other.lenient:
                return self.quantity >= other.quantity
        return False

    def __lt__(self, other: "Term") -> bool:
        if isinstance(other, self.__class__):
            if self.unit == other.unit and self.lenient == other.lenient:
                return self.quantity < other.quantity
        return False

    def __le__(self, other: "Term") -> bool:
        if isinstance(other, self.__class__):
            if self.unit == other.unit and self.lenient == other.lenient:
                return self.quantity <= other.quantity
        return False

    def change_unit(
            self, new_unit: Union[TermUnit, str], lenient: bool = False
    ) -> None:
        self.unit = new_unit
        self.lenient = lenient

    def change_unit_copy(self, new_unit: Union[TermUnit, str], lenient: bool) -> "Term":
        copy_self = deepcopy(self)
        copy_self.unit = new_unit
        copy_self.lenient = lenient
        return copy_self
