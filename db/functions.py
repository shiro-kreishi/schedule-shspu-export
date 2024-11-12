import psycopg2
from db.connect import *
from string import Template
from data.pars import Pars_minimal

time_pair = {
    1: '08:00-09:30',
    2: '09:40-11:10',
    3: '11:20-12:50',
    4: '13:20-14:50',
    5: '15:00-16:30',
    6: '16:40-18:10',
}

def search_pars_by_date(connection, date: str, auditoriums: list) -> list:
    cur = get_cursor(connection)
    query_by_date = Template('''
        select p.text, p.date, p.num, g.name from pairs p
        inner join groupsofpairs gop on p.id = gop.pair_id
        inner join "groups" g on g.id = gop.group_id 
        where p.date = '$date' 
        order by p.num asc
    ''')
    pars = []
    results = execute_sql(query_by_date.substitute(date=date), cur, all=True)
    for res in results:
        try:
            if res[0].split()[-1] in auditoriums:
                name = " ".join([s for s in res[0].replace("/ ", "").split()[:3]])
                group = res[-1]
                aud = res[0].split()[-1]
                par = Pars_minimal(name=name, group=group, auditorium=aud)
                pars.append(par)
                # print(f'{name} {group} {aud}')
                # print(res[0].replace("/ ", ""), ' | ', res[-1], ' | ', res[0].split()[-1],' | ', res[1], ' | ', time_pair[res[2]])
                # print(res[0].replace("/ ", "").split()[2:])
                # print(" ".join([s for s in res[0].replace("/ ", "").split()[2:]]))
                # print(res[0].split()[-1])
        except:
            print('IndexError: list index out of range')
            print(res)
        finally:
            pass
    
    return pars