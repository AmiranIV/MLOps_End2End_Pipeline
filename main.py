from flask import Flask, render_template, request
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Load the trained model
model = joblib.load('model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get user inputs from the form
    app_time = float(request.form['app_time'])
    website_time = float(request.form['website_time'])
    membership_time = float(request.form['membership_time'])

    # Create a pandas DataFrame with user inputs
    user_input = pd.DataFrame({
        'Time on App': [app_time],
        'Time on Website': [website_time],
        'Length of Membership': [membership_time]
    })

    # Make predictions using the loaded model
    predicted_hours = model.predict(user_input)

    # Determine the message based on the predicted hours
    if predicted_hours >= 3000:
        message = "You're addicted To Social Media!!"
    else:
        message = "You're healthy. Keep it up!"

    # Render the result.html template with the predicted hours and message
    return render_template('result.html', predicted_hours=predicted_hours, message=message)

if __name__ == '__main__':
    app.run(debug=True)
