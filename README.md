# CS50's Travel Planner
#### Video:  <[URL HERE](https://youtu.be/8FUlQKX3BMI?si=yHa2y6u42DD3eW4L)>
#### Description:

Travel Planner is a web application designed to help users plan their trips efficiently. The application allows users to register and log in to their accounts, search for flight options using the Amadeus API, and view the available flights.

## Features

- **User Registration and Login**: Users can create an account and log in to access the flight search functionality. Passwords are hashed before being stored in the database.

- **Flight Search**: Users can search for flights by entering the origin, destination, departure date, and return date. The application uses the Amadeus API to get real-time flight data based on wha the user inputted. The API integration ensures that users receive the latest flight availability and times.

- **Responsive Design**: The application has a clean and responsive design, making it accessible on different devices.

- **Pagination**: Flight search results are displayed in page format to improve usability, especially when there are alot of results.

## Files

### `app.py`
The main application file where the Flask application is configured and routes are defined. Key functionalities:

- **User Registration (`/register`)**: Handles user registration by collecting user input, hashing the password, and storing the user information in the database.

- **User Login (`/login`)**: Manages user login by validating credentials and starting session.

- **Flight Search (`/search_flights`)**: Allows users to search for flights by interacting with the Amadeus API and displays the results in a paginated format.

- **Logout (`/logout`)**: Logs the user out.

### `helpers.py`
Contains helper functions that support the main application logic:

- **get_access_token**: Retrieves the access token from the Amadeus API using the provided API key and secret. This allows for authenticating requests to the Amadeus API.

- **search_flight_offers**: Searches for flight offers using the Amadeus API and returns the flight data.

### `templates/`
Contains HTML files for rendering the user interface. Key files:

- **base.html**: The base template that includes the common layout elements such as the header and navigation. Ensures a consistent look throughout the app.

- **index.html**: The home page template that welcomes users to the application. A starting point for users.

- **register.html**: The registration page template where users can create a new account. It includes fields for entering a username, email, password, and password confirmation.

- **login.html**: The login page it includes fields for entering the email and password.

- **search_flights.html**: The template for displaying flight search results. It shows a list of available flights based on the user's search, with pages to scroll thorigh if alot of results.

### `static/styles.css`
Contains the CSS styles for the application. It includes the layout, colors, and fonts. The CSS main goal is to be responsive which works well on different devices.

## Design Choices

### Security
Security - Passwords are hashed before being stored in the database. This ensures that even if the database is compromised, the passwords remain protected. Additionally, sessions are managed securely to prevent unauthorized access.

### API Integration
The Amadeus API is integrated into the application to provide real-time flight data. This allows users to get accurate and latest information about flights. The integration is done through helper functions that handle the API requests and process the responses. The API offers a wide range of options, flight schedules, and prices.

## Database Schema
The database includes a `users` table:
- **id**
- **username**
- **email**
- **hash**

This schema ensures that user data is stored securely and efficiently.

## How to Run the Project

1. **Set Up the Environment**:
   - Install Python and pip.
   - Create a virtual environment and activate it.
   - Install the required dependencies using `pip install -r requirements.txt`.

2. **Configure the Application**:
   - Set up the database by running the necessary scripts to create the tables.
   - Obtain API credentials from Amadeus and update the application configuration with your API key and secret.

3. **Run the Application**:
   - Start the Flask development server using `flask run`.
   - Open your browser to access the application.

## Conclusion

Travel Planner is a well made and user-friendly application aimed to help people plan their trips efficiently. The app integrates secure user authentication, real-time flight search, and a responsive design, the application provides a solution for travel planning. The design choice ensure that the application is both secure and easy to use. The integration of the Amadeus API allows users to access a wide range of flight options so that they can find the best flights for their travel.
