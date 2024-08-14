import requests
from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """Decorator to ensure routes require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_access_token(api_key, api_secret):
    """Get access token from Amadeus API."""
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    token = response.json().get('access_token')
    return token

def search_flight_offers(access_token, origin, destination, departure_date, return_date):
    """Search for flight offers using Amadeus API."""
    url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'originLocationCode': origin,
        'destinationLocationCode': destination,
        'departureDate': departure_date,
        'returnDate': return_date,
        'adults': '1'
    }
    print(f"Requesting flights with params: {params}")  # Log the parameters
    response = requests.get(url, headers=headers, params=params)
    print(f"Response: {response.status_code}, {response.text}")  # Log the response
    response.raise_for_status()
    return response.json()
