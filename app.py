from random import randint
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request

from scraper import preprocess

app = Flask(__name__)
model: tf.keras.Model = tf.keras.models.load_model("model")  # type: ignore


N_HITS = 10  # number of matches to show


@app.route("/", methods=["get", "post"])
def main():
    # if there's no input, just return
    if "description" not in request.form:
        return render_template("main.j2")

    # run description through model
    description = request.form["description"]
    preprocessed_description = preprocess(description)
    predictions = model.predict([preprocessed_description])
    depts, dept_probabilities, level_predictions = predictions

    # sort level predictions from most to least likely
    levels = np.argsort(level_predictions[0])[::-1] * 100 + 100
    level_probabilities = np.sort(level_predictions[0])[::-1]

    # make a nicer format for html template
    depts = depts[0].astype(str)
    dept_probabilities = dept_probabilities[0]

    predictions = dict(
        dept=list(zip(depts, dept_probabilities)),
        level=list(zip(levels, level_probabilities)),
    )

    return render_template(
        "main.j2",
        description=description,
        randint=randint,
        predictions=predictions,
    )


if __name__ == "__main__":
    app.run()
