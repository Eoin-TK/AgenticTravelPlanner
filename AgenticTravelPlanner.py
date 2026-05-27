from typing import List
from pydantic import BaseModel

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


