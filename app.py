from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)


# =========================================================
# LOAD TRAINED ML PIPELINE
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "model",
    "stress_model.pkl"
)

model = joblib.load(MODEL_PATH)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("about.html")


# =========================================================
# PREDICTION API
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        # Prepare input data
        input_data = {
            "Gender": data["Gender"],
            "Age": float(data["Age"]),
            "City": data["City"],
            "Profession": data["Profession"],

            "Academic Pressure": float(
                data["Academic Pressure"]
            ),

            "Work Pressure": float(
                data["Work Pressure"]
            ),

            "CGPA": float(
                data["CGPA"]
            ),

            "Study Satisfaction": float(
                data["Study Satisfaction"]
            ),

            "Job Satisfaction": float(
                data["Job Satisfaction"]
            ),

            "Sleep Duration": data["Sleep Duration"],
            "Dietary Habits": data["Dietary Habits"],
            "Degree": data["Degree"],

            "Have you ever had suicidal thoughts ?": data[
                "Have you ever had suicidal thoughts ?"
            ],

            "Work/Study Hours": float(
                data["Work/Study Hours"]
            ),

            "Financial Stress": float(
                data["Financial Stress"]
            ),

            "Family History of Mental Illness": data[
                "Family History of Mental Illness"
            ]
        }

        # Convert to DataFrame
        df = pd.DataFrame([input_data])

        # =================================================
        # ML PREDICTION
        # =================================================

        prediction = model.predict(df)[0]

        probability = None

        if hasattr(model, "predict_proba"):
            probability = model.predict_proba(df)[0][1]

        # =================================================
        # CALCULATE SCORE
        # =================================================

        if probability is not None:
            score = round(probability * 100)
        else:
            score = 100 if prediction == 1 else 25

        # =================================================
        # RESULT MESSAGE
        # =================================================

        if prediction == 1:

            level = "Higher Risk"

            message = (
                "Your responses indicate patterns that may "
                "deserve additional attention and support."
            )

        else:

            level = "Lower Risk"

            message = (
                "Your responses do not indicate a higher-risk "
                "pattern according to this model."
            )

        # =================================================
        # SEND RESULT TO FRONTEND
        # =================================================

        return jsonify({
            "success": True,
            "prediction": int(prediction),
            "score": score,
            "level": level,
            "message": message
        })

    except Exception as e:

        print("Prediction Error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)