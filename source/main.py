from gflightscraper.scraper import Scraper

def run():
    """
    Example usage of the Scraper class to perform a flight search on Google Flights.

    Steps:
    1. Initialize the Scraper object to interact with Google Flights.
    2. Define the parameters for the flight search:
       - origin: The departure location (can be an IATA code or city name).
       - destination: The arrival location (can be an IATA code or city name).
       - duration: The duration of the trip in days.
       - passengers: The number of passengers for the flight.
       - search_dates: A tuple containing the start and end dates for the search (format: 'YYYY-MM-DD').
       - limit: The maximum number of flight results to return.
    3. Call the `search()` method with the specified parameters to perform the search.
    4. Print the resulting flight options returned by the search.

    Example:
    - Searching for flights from "MCZ" (Maceió) to "Santiago" with a 7-day duration, 2 passengers, 
      and a date range from '2025-08-01' to '2025-09-30', limiting the results to 1 flight.
    """
    
    # Initialize the Scraper object for Google Flights search
    flights = Scraper()

    # Define the search parameters
    origin = "MCZ"  # Departure location (IATA code or city name)
    destination = "Santiago"  # Arrival location (IATA code or city name)
    duration = 7  # Trip duration in days
    passengers = 2  # Number of passengers
    search_dates = ('2025-08-01', '2025-09-30')  # Date range for flight search
    limit = 1  # Maximum number of flight results to return

    # Perform the flight search with the specified parameters
    flights.search(origin, destination, duration, passengers, search_dates, limit)

    # Print the resulting flight options
    for f in flights.list:
        print(f)

if __name__ == "__main__":
    run()