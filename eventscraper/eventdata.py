from dataclasses import dataclass


@dataclass
class EventData:
    title: str
    location: str = ''
    description: str = ''
    url: str = ''
    start_date: str = ''
    end_date: str = ''
    organizer: str = ''
