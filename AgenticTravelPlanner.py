# IMPORT LIBRARIES
# utilities
import os
from dotenv import load_dotenv

# data gathering/handling
import requests
import pandas as pd

# type hinting
from typing import List
from pydantic import BaseModel

load_dotenv()

class Traveller(BaseModel):
    """
    A traveller with name, age, and list of interests.

    Attributes:
        name (str): The name of the traveller
        age (int): The age of the traveller
        interests (List[str])
    """
    name: str
    age: int
    interests: List[str]

class HolidayInfo(BaseModel):
    """
    Holiday information including travelers, origin, destination, duration, and month of travel.
    Attributes:
        travellers List[Traveller]: A list of travellers
        origin (str): the origin location
        destination (str): the destination location
        departureDate (str): departure date, YYYY-MM-DD
        returnDate (str): return date, YYYY-MM-DD
    """
    travellers: List[Traveller]
    origin: str
    destination: str
    departureDate: str
    returnDate: str

def skyscannerApiUrl(endpoint: str):
    return f"https://skyscanner-flights-travel-api.p.rapidapi.com/flights/{endpoint}"

def getAirport(location: str):
    """
    Retrieve airport details for a given location.

    Attributes:
        location (str): the location for which to find airport details
    """
    url = skyscannerApiUrl("searchAirport")
    querystring = {
        "market":"GB",
        "query":location,
        "locale":"en-GB"
    }

    headers = {
        "x-rapidapi-key": os.getenv("SKYSCANNER_RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("SKYSCANNER_RAPIDAPI_HOST"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()["places"][0]  

def getFlights(myTrip: HolidayInfo, currency: str ="EUR"):
    """
    Retrieve flight itineraries from skyscanner (via rapidAPI)

    Attributes:
        myTrip (HolidayInfo): trip details, see HolidayInfo definition
        currency (str): currency to use for prices, default 'EUR'
    """
    # Get airport details
    originAirport = getAirport(myTrip.origin)
    destinationAirport = getAirport(myTrip.destination)

    url = skyscannerApiUrl("searchFlights")

    querystring = {
        "childrens":str(len([t for t in myTrip.travellers if t.age < 18])),
        "adults":str(len([t for t in myTrip.travellers if t.age >= 18])),
        "originSkyId":originAirport["skyId"],
        "destinationSkyId":destinationAirport["skyId"],
        "destinationEntityId":destinationAirport["entityId"],
        "returnDate":myTrip.returnDate,
        "originEntityId":originAirport["entityId"],
        "date":myTrip.departureDate,
        "cabinClass":"economy",
        "infants":"0",
        "market":"DE",
        "currency":"EUR"
    }

    headers = {
        "x-rapidapi-key": os.getenv("SKYSCANNER_RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("SKYSCANNER_RAPIDAPI_HOST"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)

    flights_df = pd.DataFrame(response.json()["itineraries"])

    return flights_df

if __name__ == "__main__":
    myTraveller = Traveller(
        name="demo",
        age=30,
        interests=["History", "Hiking", "Fine Dining"]
    )
    myTrip = HolidayInfo(
        travellers=[myTraveller],
        origin="Cork",
        destination="Rhodes",
        departureDate="2026-07-20",
        returnDate="2026-07-27"
    )

    test_df = getFlights(myTrip=myTrip)
    
    print(test_df)