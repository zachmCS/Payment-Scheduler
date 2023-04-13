import datetime
from typing import Dict, Iterable, Optional, Protocol, Tuple, Union, runtime_checkable


@runtime_checkable
class Date(Protocol):
    """Protocol of Financial Date Class"""

    def __init__(self, day: int, month: int, year: int) -> None:
        pass

    def get_day(self) -> int:
        pass

    def get_month(self) -> int:
        pass

    def get_year(self) -> int:
        pass

    def get_julian_day(self) -> int:
        pass

    def is_leap_year(self) -> bool:
        pass

    def is_bus_day(self, calendar_input: "Calendar") -> bool:
        pass

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

    pass



@runtime_checkable
class Frequency(Protocol):
    """Protocol of Frequency Representation"""

    name: str
    term: "Term"
    numerical: float

    @property
    def year_fraction(self) -> float:
        pass

    def __str__(self) -> str:
        pass


class Calendar(Protocol):
    """Protocol of Financial Calendar class"""

    def __init__(
        self,
        weekend: Iterable[DayOfTheWeek],
        holidays: Iterable[Date],
    ) -> None:
        pass

    def __eq__(self, other: "Calendar") -> bool:
        pass

    def __str__(self) -> str:
        pass

    def add_holiday(self, date_input: Date):
        pass

    def add_holidays(self, dates_input: Iterable[Date]):
        pass

    def is_weekend(self, date_input: Date) -> bool:
        pass

    def is_holiday(self, date_input: Date) -> bool:
        pass

    def is_bus_day(
        self, date_input: Date, ignore_weekend: bool, ignore_holidays: bool
    ) -> bool:
        pass

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

