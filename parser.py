from datetime import datetime
import re
import pandas as pd

def parse_open_hours(file_path):
    """
    Parses the CSV file containing restaurant names and open hours.
    Returns a dictionary where each restaurant maps to its open/close hours for each day.
    
    Example Output:
    {
        'Restaurant A': {
            'Mon': {'open': time(11, 0), 'close': time(22, 0)},
            'Tue': {'open': time(11, 0), 'close': time(22, 0)},
            ...
        }
    }
    """
    # Days of the week as they appear in the CSV file
    days_of_week = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Initialize dictionary to store restaurant hours
    restaurant_hours = {}

    def parse_time_range(time_range):
        """
        Parses a time range string like '11:00 am - 10:00 pm' or '11 am - 10 pm'.
        Returns a dictionary with 'open' and 'close' times as datetime.time objects.
        """
        def parse_single_time(time_str):
            try:
                # Try parsing time with hours and minutes (e.g., 11:00 am)
                return datetime.strptime(time_str.strip(), "%I:%M %p").time()
            except ValueError:
                # If minutes are missing, parse with hours only (e.g., 11 am)
                return datetime.strptime(time_str.strip(), "%I %p").time()

        # Split the range into open and close times
        open_str, close_str = time_range.split('-')
        return {
            'open': parse_single_time(open_str),
            'close': parse_single_time(close_str)
        }

    def set_day_hours(day_range, time_range):
        """
        Processes a day range (e.g., 'Mon-Thu, Sun') and its time range (e.g., '11 am - 10 pm').
        Returns a dictionary mapping individual days to their open/close times.
        
        Example Input:
            day_range = 'Mon-Thu, Sun'
            time_range = '11 am - 10 pm'
        Example Output:
            {
                'Mon': {'open': time(11, 0), 'close': time(22, 0)},
                'Tue': {'open': time(11, 0), 'close': time(22, 0)},
                'Sun': {'open': time(11, 0), 'close': time(22, 0)}
            }
        """
        result = {}  # Store parsed days and times
        time_obj = parse_time_range(time_range)

        # Split days by ',' to handle mixed ranges and single days
        day_parts = day_range.split(',')
        for part in day_parts:
            part = part.strip()
            if '-' in part:  # Handle day ranges like 'Mon-Thu'
                start_day, end_day = part.split('-')
                start_idx = days_of_week.index(start_day.strip())
                end_idx = days_of_week.index(end_day.strip())
                # Assign the time range to each day in the range
                for i in range(start_idx, end_idx + 1):
                    result[days_of_week[i]] = time_obj
            else:  # Handle single days like 'Sun'
                result[part.strip()] = time_obj
        return result

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Process each row in the CSV file
    for _, row in df.iterrows():
        restaurant_name = row['Restaurant Name']  # Extract the restaurant name
        hours = row['Hours']  # Extract the hours string

        # Skip rows where 'Hours' is missing or invalid
        if not isinstance(hours, str) or pd.isna(hours):
            continue

        # Initialize a dictionary to store open/close hours for each day
        hours_dict = {day: None for day in days_of_week}

        # Split by '/' to handle multiple ranges (e.g., 'Mon-Thu 11 am - 10 pm / Fri-Sat 11 am - 11 pm')
        ranges = hours.split(' / ')
        for r in ranges:
            match = re.match(r"([A-Za-z\-, ]+)\s(.+)", r.strip())
            if match:
                day_range = match.group(1).strip()  # Extract the day range (e.g., 'Mon-Thu')
                time_range = match.group(2).strip()  # Extract the time range (e.g., '11 am - 10 pm')
                parsed_days = set_day_hours(day_range, time_range)  # Process the range
                hours_dict.update(parsed_days)  # Update the hours for the corresponding days

        # Add the parsed hours for the restaurant to the final dictionary
        restaurant_hours[restaurant_name] = hours_dict

    return restaurant_hours