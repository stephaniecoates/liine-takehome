from flask import Flask, request, jsonify
from parser import parse_open_hours
from datetime import datetime

app = Flask(__name__)

# Load and parse restaurant data
restaurant_data = parse_open_hours("restaurants.csv")

@app.route('/open-restaurants', methods=['GET'])


def get_open_restaurants():
    """
    Endpoint to return a list of restaurants open at the specified datetime.
    """
    datetime_str = request.args.get('datetime')  # Query parameter input

    # Handle missing datetime parameter
    if not datetime_str:
        return jsonify({"error": "Missing 'datetime' parameter"}), 400

    try:
        # Parse input datetime string to a datetime object
        input_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Extract the day of the week (e.g., 'Mon') and time
        day_of_week = input_datetime.strftime("%a")  # 'Mon', 'Tues', etc.
        current_time = input_datetime.time()         # Extract the time part

        # Filter restaurants that are open at the specified time
        open_restaurants = []
        for restaurant_name, hours in restaurant_data.items():
            day_hours = hours.get(day_of_week)  # Get hours for the specific day
            if day_hours and day_hours['open'] <= current_time <= day_hours['close']:
                open_restaurants.append(restaurant_name)

        # Return the list of open restaurants
        return jsonify({"open_restaurants": open_restaurants})

    except ValueError:
        # Handle invalid datetime format
        return jsonify({"error": "Invalid datetime format. Use 'YYYY-MM-DD HH:MM'"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
