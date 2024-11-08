from db.connect import *
from string import Template
from data.pars import Pars_minimal, Pars_with_date_and_time
from datetime import datetime


class Searcher:
    
    def __init__(self, connection):
        self.cursor = get_cursor(conn=connection)
    
    time_pair = {
        1: '08:00-09:30',
        2: '09:40-11:10',
        3: '11:20-12:50',
        4: '13:20-14:50',
        5: '15:00-16:30',
        6: '16:40-18:10',
    }

    query_by_date = Template('''
        select p.text, p.date, p.num, g.name from pairs p
        inner join groupsofpairs gop on p.id = gop.pair_id
        inner join "groups" g on g.id = gop.group_id 
        where p.date = '$date' 
        order by p.num asc
    ''')

    def by_date(self, date: str, auditoriums: list, func) -> list:
        pairs = []
        results = execute_sql(self.query_by_date.substitute(date=date), self.cursor, all=True)
        for res in results:
            try:
                if res[0].split()[-1] in auditoriums:
                    pair = func(res)
                    pairs.append(pair)
            except:
                print('IndexError: list index out of range')
                print(res)
            finally:
                pass
    
        return pairs
    
    def create_minimal_pair(self, res) -> Pars_minimal:
        name = " ".join([s for s in res[0].replace("/ ", "").split()[:3]])
        group = res[-1]
        aud = res[0].split()[-1]
        pair = Pars_minimal(name=name, group=group, auditorium=aud)
        return pair
    
    def create_pair_with_date_and_time(self, res) -> Pars_with_date_and_time:
        name = " ".join([s for s in res[0].replace("/ ", "").split()[:3]])
        group = res[-1]
        aud = res[0].split()[-1]
        p_date = res[1]
        p_time = self.time_pair[res[2]]
        pair = Pars_with_date_and_time(
            name=name, group=group, auditorium=aud,
            date=p_date, timestamp=p_time
        )
        return pair
