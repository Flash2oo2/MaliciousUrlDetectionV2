from flask import Flask, render_template, request, jsonify
from utils import model_predict

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("content")
    prediction = model_predict(url)
    return render_template("index2.html", prediction=prediction, url=url)


# Create an API endpoint
@app.route("/api/predict", methods=["POST"])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    url = data["content"]
    prediction = model_predict(url)
    return jsonify({"prediction": prediction, "url": url})  # Return prediction


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
