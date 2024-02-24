from flask import Flask, render_template, jsonify
from twilio.rest import Client
import geocoder

app = Flask(__name__)

account_sid = 'AC194204e5d3e9532978a39eb190ad4960'

auth_token = '196102f5fa3a53fc48460224b280c077'

twilio_phone_number = '+12052705339'

recipient_phone_number = '+917702014320'

def send_location_sms(latitude, longitude):

    client = Client(account_sid, auth_token)

    location_message = f"Latitude: {latitude}, Longitude: {longitude}"

    try:
        message = client.messages.create(
            body=location_message,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        return f"Message sent. SID: {message.sid}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def index():
    try:
        location_ip = geocoder.ip('me')
        latitude = location_ip.latlng[0]
        longitude = location_ip.latlng[1]

        location_message = f"Latitude: {latitude}, Longitude: {longitude}"

        return render_template('index.html', location_message=location_message)

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/send_location')
def send_location():
    try:
        location_ip = geocoder.ip('me')
        latitude = location_ip.latlng[0]
        longitude = location_ip.latlng[1]
        
        result = send_location_sms(latitude, longitude)

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'result': f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
