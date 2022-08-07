from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from application import db
import joblib
import pandas as pd


model = Blueprint('machine', __name__)

#Create
@model.route('/predict', methods = ['GET','POST'])
@login_required
def predict():
    if request.method == "POST":
        reg = joblib.load("application/model/reg.pkl")

        # Get values through the form
        age = request.form.get("age")
        food_consumed = request.form.get("food_consumed")
        num_of_chickiens = request.form.get("num_of_chickiens")
        dead = request.form.get("dead")

        # Put inputs to dataframe
        X = pd.DataFrame([[age, food_consumed, num_of_chickiens, dead]], columns = ["Age", "FoodConsumed", "NumOfChickiens", "Dead"])

        # Get prediction
        prediction = reg.predict(X)[0]

    else:
            prediction = ""

    return render_template("prediction.html", output = 'Predicted amount of eggs is: {}'.format(prediction))
