from db.connect import *
from string import Template
from data.pars import Pars_minimal, Pars_with_date_and_time
from datetime import datetime, timedelta


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

    def execute_query(self, query: Template, auditoriums, func) -> list:
        results = execute_sql(query, self.cursor, all=True)
        pairs = []
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

    def by_date(self, date: datetime, auditoriums: list, func) -> list:
        query_by_date = Template('''
        select p.text, p.date, p.num, g.name from pairs p
        inner join groupsofpairs gop on p.id = gop.pair_id
        inner join "groups" g on g.id = gop.group_id 
        where p.date = '$date' 
        order by p.date asc
        ''')
        
        return self.execute_query(
            query_by_date.substitute(date=str(date)),
            auditoriums, func
        )
    
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
    
    def by_range_of_dates(self, start_date:datetime, end_date:datetime, auditoriums: list, func) -> list:
        pairs = []
        query_by_dates = Template('''
        select p.text, p.date, p.num, g.name from pairs p
        inner join groupsofpairs gop on p.id = gop.pair_id
        inner join "groups" g on g.id = gop.group_id 
        where p.date >= '$start_date' and p.date <= '$end_date'
        order by p.date asc
        ''')
        
        return self.execute_query(
            query_by_dates.substitute(start_date=str(start_date), end_date=str(end_date)),
            auditoriums, func
        )
