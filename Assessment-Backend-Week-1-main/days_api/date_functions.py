"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    """
    Takes a date in string format, and returns a 
    datetime object in the DD.MM.YYYY format
    """
    if type(date) != str:
        return {"error": True, "message":
                "'date' needs to be a string."}

    result = datetime.strptime(date, "%d.%m.%Y")

    return result


def get_days_between(first: datetime, last: datetime) -> int:
    """
    Takes 2 datetime objects, and finds the number of days
    between them
    """
    if type(first) or type(last) != datetime:
        return {"error": True, "message":
                "first date and last date need to be datetime objects."}

    if last < first:
        return {"error": True, "message":
                "Your first date needs to be earlier than your last date."
                }

    day_diff = (last - first).days

    return day_diff


def get_day_of_week_on(date: datetime) -> str:
    """Returns the day of the week that a given date is on"""
    if type(date) != datetime:
        return {"error": True, "message":
                "'date' needs to be a datetime object"}

    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
            3: "Thursday", 4: "Friday", 5: "Saturday",
            6: "Sunday"}

    day_index = date.weekday()

    return days[day_index]
