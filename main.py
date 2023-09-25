from db.connect import *
from string import Template
import os
from dotenv import load_dotenv

time_pair = {
    1: '08:00-09:30',
    2: '09:40-11:10',
    3: '11:20-12:50',
    4: '13:20-14:50',
    5: '15:00-16:30',
    6: '16:40-18:10',
}

technopark_auditoriums = [
    '232А', '233А', '234А', '235А', '128А', '129А', '201В', 
]

def main():
    
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    db = os.getenv('DATABASE_PG')
    user = os.getenv('USER_PG')
    password = os.getenv('PASSWORD_PG')
    host = os.getenv('HOST_PG')
    port = os.getenv('PORT_PG')

    conn = get_connection(
        db=db, user=user, password=password,
        host=host, port=port
    )
    cur = get_cursor(conn)
    query_by_date = Template('''
        select p.text, p.date, p.num, g.name from pairs p
        inner join groupsofpairs gop on p.id = gop.pair_id
        inner join "groups" g on g.id = gop.group_id 
        where p.date = '$date' 
        order by p.num asc
    ''')

    results = execute_sql(query_by_date.substitute(date='2023-09-26'), cur, all=True)
    for res in results:
        # print(res[0].split())
        try:
            if res[0].split()[-1] in technopark_auditoriums:
                print(res[0].replace("/ ", ""), ' | ', res[len(res)-1], ' | ', res[0].split()[-1],' | ', res[1], ' | ', time_pair[res[2]])
        except:
            print('IndexError: list index out of range')
        finally:
            pass
    close_connection(conn)

if __name__=='__main__':
    main()