from datetime import datetime

class Pars_minimal:
    def __init__(self, name: str, group: str, auditorium: str):
        self.name = name
        self.group = group
        self.auditorium = auditorium
    
    def __str__(self):
        return f'{self.name} {self.group} {self.auditorium}'
    

class Pars_with_date_and_time(Pars_minimal):
    def __init__(self, name: str, group: str, auditorium: str, date: datetime.date, timestamp: str):
        self.date = date
        self.timestamp = timestamp
        
        super().__init__(name, group, auditorium)

    def __str__(self):
        return f'{super().__str__()} {self.date} {self.timestamp}'