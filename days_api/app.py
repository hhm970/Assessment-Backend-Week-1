"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, Response, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between


def error_invalid_method_405():
    """Returns an error message for status code 405 in json format."""
    result = {"error": True, "message":
              "Invalid request method used."}

    return jsonify(result), 405


ERROR_DATE_NOT_STR = {"error": True, "message":
                      "'date' needs to be a string."
                      }
ERROR_DATE_INPUT_WRONG_FORMAT = {"error": True, "message":
                                 "'date_input' should be in '%d.%m.%Y' format."
                                 }
ERROR_PATH_PARAMETER_NOT_PROVIDED = {"error": "Missing required data."}
ERROR_BETWEEN_DATES_NOT_DATETIME = {
    "error": "Unable to convert value to datetime."}
ERROR_BETWEEN_FIRST_LAST_WRONG = {"error": True, "message":
                                  "Your first date needs to be earlier than your last date."
                                  }

ERROR_WEEKDAY_DATE_NOT_DATETIME = {"error": True, "message":
                                   "'date' needs to be a datetime object."
                                   }
ERROR_HISTORY_NUMBER_TOO_BIG = {"error": True, "message":
                                "'number' cannot be greater than the number of previous API requests."
                                }


global app_history
app_history = []


app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."}), 200


@app.route("/between", methods=["POST"])
def days_between():
    """Returns the number of days between two dates."""

    if request.method == "POST":

        data = request.json

        first = data.get("first")
        last = data.get("last")

        if first or last is None:
            return jsonify(ERROR_PATH_PARAMETER_NOT_PROVIDED), 400

            return jsonify(ERROR_BETWEEN_DATES_NOT_DATETIME), 400

        first_date = convert_to_datetime(first)
        last_date = convert_to_datetime(last)

        if first_date or last_date == ERROR_DATE_NOT_STR:
            return jsonify(ERROR_DATE_NOT_STR), 400

        # if first_date or last_date == ERROR_DATE_INPUT_WRONG_FORMAT:
        #    return jsonify(ERROR_DATE_INPUT_WRONG_FORMAT), 400

        days_number = get_days_between(first_date, last_date)

        # if days_number == ERROR_BETWEEN_DATES_NOT_DATETIME:
        #    return jsonify(days_number), 400

        # if days_number == ERROR_BETWEEN_FIRST_LAST_WRONG:
        #    return jsonify(days_number), 400

        result = {"days": days_number}

        add_to_history(request)

        return jsonify(result), 200

    return error_invalid_method_405


@app.route("/weekday", methods=["POST"])
def day_weekday():
    """Returns the day of the week a specific date is."""

    if request.method == "POST":

        data = request.json

        date_input = data.get("date")

        if date_input is None:
            return jsonify(ERROR_PATH_PARAMETER_NOT_PROVIDED), 400

        date = convert_to_datetime(date_input)
        if date == ERROR_DATE_NOT_STR:
            return jsonify(date), 400

        if date == ERROR_DATE_INPUT_WRONG_FORMAT:
            return jsonify(date), 400

        day_of_week = get_day_of_week_on(date)

        if day_of_week == ERROR_WEEKDAY_DATE_NOT_DATETIME:
            return jsonify(day_of_week), 400

        result = {"weekday": day_of_week}

        add_to_history(request)

        return jsonify(result), 200

    return error_invalid_method_405


@app.route("/history", methods=["GET", "DELETE"])
def get_history():
    """
    POST: Returns the previous requests to the API of 
    a given quantity.
    """
    args = request.args.to_dict()
    number = args.get("number")

    if request.method == "GET":
        m = len(app_history)

        if number is None:
            number = 5

        if number > m:
            return jsonify(ERROR_HISTORY_NUMBER_TOO_BIG), 400

        else:
            i = m - number + 1
            result = app_history[i:]

            add_to_history(request)

            return jsonify(result), 200

    if request.method == "DELETE":

        app_history = list()

        return jsonify({"status": "History cleared"})

    if request.method not in {"POST", "DELETE"}:

        return error_invalid_method_405


if __name__ == "__main__":

    app.run(port=8080, debug=True)
