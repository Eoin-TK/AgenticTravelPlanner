#IMPORT LIBRARIES
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
        duration (int): number of nights
        month (str): the month of travel
    """
    travellers: List[Traveller]
    origin: str
    destination: str
    month: str

def getFlights(originID: str, destinationID: str, fromDate: str, returnFromDate: str, currency: str ="EUR"):
    """
    Retrieve flight prices from skyscanner (via rapidAPI)

    Attributes:
        originID (str): ID of origin airport
        destinationID (str): ID of destination airport
        fromDate (str): earliest option for date of outbound flight, YYYY-MM-DD
        returnFromDate (str): earliest option for date of return flight, YYYY-MM-DD
        currency (str): currency to retrieve prices in
    """
    url = os.getenv("SKYSCANNER_RAPIDAPI_URL")
    querystring = {
        "originSkyId":originID,
        "returnFromDate":returnFromDate,
        "currency":currency,
        "fromDate":fromDate,
        "destinationSkyId":destinationID
    }
    
    headers = {
        "x-rapidapi-key": os.getenv("SKYSCANNER_RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("SKYSCANNER_RAPIDAPI_HOST"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)

    inboundFlights_df = pd.DataFrame(response.json()["outboundDates"])
    outboundFlights_df = pd.DataFrame(response.json()["inboundDates"])

    return outboundFlights_df, inboundFlights_df

