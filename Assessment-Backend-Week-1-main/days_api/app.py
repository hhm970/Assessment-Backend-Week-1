"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, Response, request, jsonify

from date_functions import convert_to_datetime, get_day_of_week_on, get_days_between

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
def days_between(first: str, last: str):
    """Returns the number of days between two dates."""

    if request.method == "POST":

        first_date = convert_to_datetime(first)
        last_date = convert_to_datetime(last)

        days_number = get_days_between(first_date, last_date)

        result = {"days": days_number}

        return jsonify(result), 200

    else:

        result = {"error": True, "message":
                  "Invalid request method used."}

        return jsonify(result), 405


@app.route("/weekday", methods=["GET"])
def day_weekday(date_input: str):
    """Returns the day of the week a specific date is."""

    if request.method == "GET":

        date = convert_to_datetime(date_input)

        day_of_week = get_day_of_week_on(date)

        result = {"weekday": day_of_week}

        return jsonify(result), 200

    else:

        result = {"error": True, "message":
                  "Invalid request method used."}

        return jsonify(result), 405


@app.route("/history", methods=["POST", "DELETE"])
def get_history(number: int = 5):
    """
    POST: Returns the previous requests to the API of 
    a given quantity.
    """

    if request.method == "POST":
        m = len(app_history)

        if number > m:
            result = {"error": True, "message":
                      "'number' cannot be greater than the number of previous API requests."}

            return jsonify(result), 400

        else:
            i = m - number + 1
            result = app_history[i:]

            return jsonify(result), 200

    if request.method == "DELETE":

        app_history = list()

        return jsonify({"status": "History cleared"})

    if request.method not in {"POST", "DELETE"}:

        result = {"error": True, "message":
                  "Invalid request method used."}

        return jsonify(result), 405


if __name__ == "__main__":
    app.run(port=8080, debug=True)
