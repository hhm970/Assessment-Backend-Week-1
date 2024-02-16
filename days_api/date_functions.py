"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    """
    Takes a date in string format, and returns a 
    datetime object in the DD.MM.YYYY format
    """
    if not isinstance(date, str):
        raise TypeError("'date' needs to be a string.")

    if (date[2] and date[-5]) != ".":
        raise ValueError("Unable to convert value to datetime.")

    result = datetime.strptime(date, "%d.%m.%Y")

    return result


def get_days_between(first: datetime, last: datetime) -> int:
    """
    Takes 2 datetime objects, and finds the number of days
    between them
    """
    if not (isinstance(first, datetime) and isinstance(last, datetime)):
        raise TypeError("Datetimes required.")

    day_diff = (last - first).days

    return day_diff


def get_day_of_week_on(date: datetime) -> str:
    """Returns the day of the week that a given date is on"""

    if not isinstance(date, datetime):
        raise TypeError("Datetime required.")

    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
            3: "Thursday", 4: "Friday", 5: "Saturday",
            6: "Sunday"}

    day_index = date.weekday()

    return days[day_index]
