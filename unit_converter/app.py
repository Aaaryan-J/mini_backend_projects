from math import isfinite

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

UNITS = {
    "length": ['meters', 'kilometers', 'miles'],
    "weight": ['grams', 'kilograms', 'pounds'],
    "temperature": ['celsius', 'fahrenheit', 'kelvin']
}

def convert(measurement, from_unit, to_unit, value):
    if measurement == "length":
        to_meters = {"meters": 1, "kilometers": 1000, "miles": 1609.344}
        base_value = value * to_meters[from_unit]
        return base_value / to_meters[to_unit]

    if measurement == "weight":
        to_grams = {"grams": 1, "kilograms": 1000, "pounds": 453.59237}
        base_value = value * to_grams[from_unit]
        return base_value / to_grams[to_unit]

    if measurement == "temperature":
        if from_unit == "fahrenheit":
            value = (value - 32) * 5 / 9
        elif from_unit == "kelvin":
            value -= 273.15

        if to_unit == "fahrenheit":
            return value * 9 / 5 + 32
        if to_unit == "kelvin":
            return value + 273.15
        return value

    return None


def render_converter(measurement):
    from_unit = request.form.get("from_unit")
    to_unit = request.form.get("to_unit")
    value_text = request.form.get("value")
    error = None
    result = None

    if from_unit not in UNITS[measurement]:
        error = "Invalid source unit."
    elif to_unit not in UNITS[measurement]:
        error = "Invalid target unit."
    elif not value_text:
        error = "Please enter a value."
    else:
        try:
            value = float(value_text)
            if not isfinite(value):
                raise ValueError
            result = round(convert(measurement, from_unit, to_unit, value), 2)
        except ValueError:
            error = "Please enter a valid number."

    return render_template(
        "index.html",
        value=value_text,
        result=result,
        error=error,
        measurement=measurement,
        units=UNITS.get(measurement, []),
        from_unit=from_unit,
        to_unit=to_unit,
    )


@app.route("/")
def index():
    return redirect(url_for("length"))


@app.route("/length", methods=["GET", "POST"])
def length():
    return render_converter("length")


@app.route("/weight", methods=["GET", "POST"])
def weight():
    return render_converter("weight")


@app.route("/temperature", methods=["GET", "POST"])
def temperature():
    return render_converter("temperature")