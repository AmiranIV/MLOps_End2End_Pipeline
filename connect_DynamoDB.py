from flask import Flask, render_template, request
import pandas as pd
import joblib
import boto3
from datetime import datetime

###### BEFORE YOU ADD THE DYNAMO DB YOU NEED TO AUTHENTICATE ****OUTSIDE THE CODE WITH AWS!!!######################
###### pip install boto3 >>>>>>> IN YOUR ENVIORMENT!##########
###### aws configure in your pc with private and public Secret keys >>>>>>>> INTERMINAL SESSION##############
app = Flask(__name__)

# Load the trained model
model = joblib.load('model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        app_time = float(request.form['app_time'])
        website_time = float(request.form['website_time'])
        membership_time = float(request.form['membership_time'])
        if app_time <= 0 or website_time <= 0 or membership_time <= 0:
            raise ValueError
    except ValueError:
        return "Please Enter Only Positive Numbers."

    # Create a pandas DataFrame with user inputs
    user_input = pd.DataFrame({
        'Time on App': [app_time],
        'Time on Website': [website_time],
        'Length of Membership': [membership_time]
    })

    # Make predictions using the loaded model
    predicted_hours = model.predict(user_input)

    if predicted_hours >= 3000:
        message = "You're addicted to social media!"
        addiction_status = "Addicted"
    else:
        message = "You're healthy. Keep it up!"
        addiction_status = "Not Addicted"


    user_ip = str(request.remote_addr)
    date_created = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    upload_data = {
        'IP': user_ip,
        'Date': date_created,
        'Addiction Status': addiction_status,
        'Time on App': int(app_time),
        'Time on Website': int(website_time),
        'Length of Membership': int(membership_time)
    }

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('YOUR TABLE NAME')
    dynamoTable.put_item(Item=upload_data)

    # Render the result.html template with the predicted hours, message, and addiction status
    return render_template('result.html', predicted_hours=predicted_hours, message=message)

if __name__ == '__main__':
    app.run(debug=True)

