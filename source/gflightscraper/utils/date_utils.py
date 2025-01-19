from datetime import datetime, timedelta

def calculate_date_ranges(start, end):
        """
        Calculates the date ranges based on the start and end dates provided. 
        If the date range exceeds 199 days, it splits the range into two parts.
        
        Parameters:
            start (str): The start date for the range.
            end (str): The end date for the range.

        Returns:
            list: A list of tuples representing the date ranges.
        """
        today = datetime.now()
        
        max_date = today + timedelta(days=330)

        # Parse the input dates
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        # You can't start with a date earlier than today
        if start_date < today:
            start_date = today

        # Calculate the total days in the custom range
        total_days_in_range = (min(max_date, end_date) - start_date).days

        # Split the range based on the logic
        if total_days_in_range <= 199:
            date_ranges = [
                (start_date.strftime("%Y-%m-%d"), min(max_date, end_date).strftime("%Y-%m-%d"))
            ]
        else:
            date_ranges = [
                (start_date.strftime("%Y-%m-%d"), (start_date + timedelta(days=199)).strftime("%Y-%m-%d")), 
                ((start_date + timedelta(days=200)).strftime("%Y-%m-%d"), min(max_date, end_date).strftime("%Y-%m-%d"))
            ]
        return date_ranges
