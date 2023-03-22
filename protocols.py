import datetime
import selftime
from typing import Dict, Iterable, Optional, Protocol, Tuple, Union, runtime_checkable
import holidays
from jdcal import gcal2jd, is_leap


@runtime_checkable
class Date(Protocol):
    """Protocol of Financial Date Class"""

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

    def get_day(self) -> int:
        return self.day

    def get_month(self) -> int:
        return self.month

    def get_year(self) -> int:
        return self.year

    def get_julian_day(self) -> int:
        jyear = gcal2jd(self.year, self.month, self.day)
        jyear = jyear[0] + jyear[1] + 0.5
        return jyear

    def is_leap_year(self) -> bool:
        return is_leap(self.year)

    def is_bus_day(self, calendar_input: "Calendar") -> bool:
        # what to do with calendar?

        if self.day in holidays.WEEKEND or self.day in us_holidays:
            return false
        else:
            return true

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def __hash__(self) -> int:
        pass

    def __add__(self, other: Union[int, "Frequency", "Term"]) -> "Date":
        pass

    def __sub__(self, other: Union[int, "Frequency", "Term"]) -> "Date":
        pass

    def __eq__(self, other: "Date") -> bool:
        pass

    def __gt__(self, other: "Date") -> bool:
        pass

    def __ge__(self, other: "Date") -> bool:
        pass

    def __lt__(self, other: "Date") -> bool:
        pass

    def __le__(self, other: "Date") -> bool:
        pass


class BusinessDayRule(Protocol):
    """Protocol of Business Day Rule Representation"""

    # need to add more to protocol 
    def next_bus_day(self) -> date:  # after calculating what exact day a payment should fall on, this function will
        # either return that self if it is a business day, or the next business day if it is a weekend or holiday
        bus_self = datetime.date(get_year(self), get_month(self), get_day(self))
        us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for\
        while bus_self.weekday() in holidays.WEEKEND or bus_self in us_holidays:
            bus_self += timedelta(days=1)
        return bus_self

    @property
    def prev_bus_day(self) -> date:  # after calculating what exact day a payment should fall on, this function will
        # either return that self if it is a business day, or the previous business day if it is a weekend or holiday
        us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
        bus_self = datetime.date(get_year(self), get_month(self), get_day(self))
        while bus_self.weekday() in holidays.WEEKEND or bus_self in us_holidays:
            bus_self -= timedelta(days=1)
        return bus_self

    def prev_bus_day_modded(
            self) -> date:  # after calculating what exact day a payment should fall on, this function will
        # either return that self if it is a business day, or the previous business day
        # if it is a weekend or holiday stopping at the first day of the month
        bus_self = datetime.date(get_year(self), get_month(self), get_day(self))
        us_holidays = holidays.UnitedStates()  # can change this to whatever financal institution/region to account for
        while bus_self.weekday() in holidays.WEEKEND or bus_self in us_holidays:
            if (bus_self - timedelta(days=1)).month == bus_self.month:
                bus_self -= timedelta(days=1)
            else:
                next_bus_day_modded(bus_self)

        return bus_self

    def next_bus_day_modded(
            self) -> datetime:  # after calculating what exact day a payment should fall on, this function will
        # either return that self if it is a business day, or the next business day if
        # it is a weekend or holiday stopping at the last day of the month
        bus_self = datetime.date(get_year(self), get_month(self), get_day(self))
        us_holidays = holidaygis.UnitedStates()  # can change this to whatever institution/region to account for
        while bus_self.weekday() in holidays.WEEKEND or bus_self in us_holidays:
            if (bus_self + timedelta(days=1)).month == bus_self.month:
                bus_self += timedelta(days=1)
            else:
                prev_bus_day_modded(bus_self)
        return bus_self

    pass


@runtime_checkable
class Frequency(Protocol):
    """Protocol of Frequency Representation"""

    name: str
    term: "Term"
    numerical: float

    @property
    def year_fraction(self) -> float:
        start = selftime.self(get_year(self), 1, 1).toordinal()
        year_length = selftime.self(get_year(self) + 1, 1, 1).toordinal() - start
        return get_year(self) + float(self.toordinal() - start) / year_length

    def __str__(self) -> str:
        pass


class Calendar(Protocol):
    """Protocol of Financial Calendar class"""

    def __init__(
            self,
            weekend: Iterable[DayOfTheWeek],
            holidays: Iterable[Date],
    ) -> None:
        """
        :param weekend: weekend for current calender
        :param holidays: holidays for current calender
        """
        self.weekend = weekend
        self.holidays = holidays

    def __eq__(self, other: "Calendar") -> bool:
        pass

    def __str__(self) -> str:
        pass

    def add_holiday(self, self_input: Date):
        pass

    def add_holidays(self, self_input: Iterable[Date]):
        pass

    def is_weekend(self, self_input: Date) -> bool:
        if get_day(self) not in holidays.WEEKEND:
            return false
        else:
            return true

    def is_holiday(self, self_input: Date) -> bool:
        if datetime.date(get_year(self), get_month(self), get_day(self)) not in us_holidays:
            return false
        else:
            return true

    # checks the ignore bools to return the correct check to see if it is a buisness day
    # if both ignore bools are false then is_holiday and is_weekend need to be checked
    # if both are true then everyday is a buisness holiday and return will always be true
    def is_bus_day(
            self, self_input: Date, ignore_weekend: bool, ignore_holidays: bool
    ) -> bool:
        if not ignore_weekend and not ignore_holidays:
            if is_holiday(self) or is_weekend(self):
                return false
            else:
                return true
        elif not ignore_weekend:
            if is_weekend(self):
                return false
            else:
                return true
        elif not ignore_holidays:
            if is_holiday(self):
                return false
            else:
                return true
        else:
            return true

    def bus_to_cal_day(
            self,
            self_input: Date,
            term_input: "Term",
            business_day_rule: BusinessDayRule,
            ignore_weekend: bool,
            ignore_holidays: bool,
    ) -> "Term":
        pass

    def business_days_between(
            self,
            start_self: Date,
            end_self: Date,
            ignore_weekend: bool,
            ignore_holidays: bool,
    ) -> int:
        pass


class TermUnit(Protocol):
    """Protocol of Term Unit Representation"""

    name: str
    code: str

    def __str__(self) -> str:
        pass


@runtime_checkable
class Term(Protocol):
    """Financial Term Class"""

    quantity: int
    unit: TermUnit

    CODE_TO_TERM_MAP: Dict[str, TermUnit]

    def __init__(
            self, quantity: int, unit: Union[TermUnit, str], lenient: bool = False
    ) -> None:
        pass

    @classmethod
    def from_str(cls, string: str, lenient: bool = False) -> "Term":
        pass

    def __str__(self) -> str:
        pass

    def __float__(self) -> float:
        pass

    def __repr__(self) -> str:
        pass

    def __hash__(self) -> int:
        pass

    def __add__(self, other: "Term") -> "Term":
        pass

    def __sub__(self, other: "Term") -> "Term":
        pass

    def __mul__(self, other: int) -> "Term":
        pass

    def __floordiv__(self, other: int) -> "Term":
        pass

    def __mod__(self, other: int) -> "Term":
        pass

    def __truediv__(self, other: int) -> "Term":
        pass

    def __eq__(self, other: "Term") -> bool:
        pass

    def __gt__(self, other: "Term") -> bool:
        pass

    def __ge__(self, other: "Term") -> bool:
        pass

    def __lt__(self, other: "Term") -> bool:
        pass

    def __le__(self, other: "Term") -> bool:
        pass

    def change_unit(
            self, new_unit: Union[TermUnit, str], lenient: bool = False
    ) -> None:
        pass

    def change_unit_copy(self, new_unit: Union[TermUnit, str], lenient: bool) -> "Term":
        pass
