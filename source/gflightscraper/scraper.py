import json
from collections import namedtuple
from gflightscraper.utils.api_utils import make_post_request
from gflightscraper.utils.date_utils import calculate_date_ranges
from unidecode import unidecode

class Scraper:
    def __init__(self):
        self.API = "https://www.google.com/_/FlightsFrontendUi/data/"
        self.list = []
        self.flight = namedtuple('Flight', ['origin', 'destination', 'date_from', 'date_to', 'price', 'duration', 'passengers'])
        self.departure = namedtuple('Departure', ['code', 'price', 'airline', 'stops_count', 'stops_list'])

    def search(self, origin_iata, destination_iata, duration, passengers, dates, limit=0):
        """
        Searches for flights between the origin and destination within the specified date range.
        
        Parameters:
            origin_iata (str): The IATA code of the origin airport.
            destination_iata (str): The IATA code of the destination airport.
            duration (int): The duration of the trip in days.
            passengers (int): The number of passengers.
            dates (tuple): A tuple containing the start and end dates for the search.
            limit (int): The limit of the results, defualt is 0 (no limits)

        Returns:
            list: A list of the cheapest flights available.
        """
        date_ranges = calculate_date_ranges(dates[0], dates[1])
        self.origin = self.__get_city_by_iata(origin_iata)
        self.destination = self.__get_city_by_iata(destination_iata)
        for start, end in date_ranges:
            payload = f"f.req=%5Bnull%2C%22%5Bnull%2C%5Bnull%2Cnull%2C1%2Cnull%2C%5B%5D%2C1%2C%5B{passengers}%2C0%2C0%2C0%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B%5B%5B%5B%5C%22%2Fm%2F{self.origin.code}%5C%22%2C4%5D%5D%5D%2C%5B%5B%5B%5C%22%2Fm%2F{self.destination.code}%5C%22%2C4%5D%5D%5D%2Cnull%2C0%5D%2C%5B%5B%5B%5B%5C%22%2Fm%2F{self.destination.code}%5C%22%2C4%5D%5D%5D%2C%5B%5B%5B%5C%22%2Fm%2F{self.origin.code}%5C%22%2C4%5D%5D%5D%2Cnull%2C0%5D%5D%2Cnull%2Cnull%2Cnull%2C1%5D%2C%5B%5C%22{start}%5C%22%2C%5C%22{end}%5C%22%5D%2Cnull%2C%5B{duration}%2C{duration}%5D%5D%22%5D"
            response = make_post_request(f"{self.API}travel.frontend.flights.FlightsFrontendService/GetCalendarPicker", payload)
            self.__parse_flights(response, duration, passengers)

        self.list.sort(key=lambda x: x.price)
        if limit > 0:
            self.list = self.list[:limit]
        return self.list
    
    def __parse_flights(self, response, duration, passengers):
        data = json.loads(response)
        for item in data:
            if "wrb.fr" not in item:
                continue
            nested_json = json.loads(item[2])
            if len(nested_json) == 1:
                continue
            for entry in nested_json[1]:
                if entry[2] is None:
                    continue
                price = entry[2][0][1]
                self.list.append(self.flight(self.origin.name, self.destination.name, entry[0], entry[1], price, duration, passengers))


    def __get_city_by_iata(self, iata_or_name):
        """
        Retrieves city information (name, code, and IATA) based on the provided IATA code or city name.
        
        Parameters:
            iata_or_name (str): The IATA code or name of the city.

        Returns:
            namedtuple: A namedtuple containing the city name, code, and IATA code.
        """
        payload = f"f.req=%5B%5B%5B%22H028ib%22%2C%22%5B%5C%22{iata_or_name}%5C%22%2C%5B1%2C2%2C3%2C5%2C4%5D%2Cnull%2C%5B1%2C1%2C1%5D%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
        response = make_post_request(f"{self.API}batchexecute", payload)
        data = json.loads(response)
        city_data = json.loads(data[0][2])[0][0][0]
        return namedtuple('City', ['name', 'code', 'iata'])(city_data[2], city_data[4].split("/")[-1], city_data[5])