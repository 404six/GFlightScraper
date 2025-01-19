import json
from collections import namedtuple

class Scraper:
    def __init__(self):
        self.API = "https://www.google.com/_/FlightsFrontendUi/data/"
        self.list = []
        self.flight = namedtuple('Flight', ['origin', 'destination', 'date_from', 'date_to', 'price', 'duration', 'passengers'])
        self.departure = namedtuple('Departure', ['code', 'price', 'airline', 'stops_count', 'stops_list'])
