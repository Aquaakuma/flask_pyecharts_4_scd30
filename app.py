from flask import Flask, render_template

from makechart import chart_json, ReadCSV, grid_chart


app = Flask(__name__, static_folder="templates")

csvfile = "./Data/data.csv"


def charts_base():
    Chart = grid_chart(ReadCSV(csvfile))
    return Chart


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Chart")
def get_chart():
    c = charts_base()
    return c



@app.route("/DynamicData")
def update_data():
    json_data = chart_json(ReadCSV(csvfile))
    return json_data

if __name__ == "__main__":
    app.run(debug=True)
