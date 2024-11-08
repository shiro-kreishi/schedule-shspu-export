class Pars_minimal:
    def __init__(self, name: str, group: str, auditorium: str):
        self.name = name
        self.group = group
        self.auditorium = auditorium
    
    def __str__(self):
        return f'{self.name} {self.group} {self.auditorium}'