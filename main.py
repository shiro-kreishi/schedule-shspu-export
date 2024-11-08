from db.connect import *
from string import Template
import os
from dotenv import load_dotenv
from sys import argv
from db.functions import search_pars_by_date
from db.serach import Searcher

time_pair = {
    1: '08:00-09:30',
    2: '09:40-11:10',
    3: '11:20-12:50',
    4: '13:20-14:50',
    5: '15:00-16:30',
    6: '16:40-18:10',
}

technopark_auditoriums = [
    '232А', '233А', '234А', '235А', '128А', '129А', '201В', '217В', 
]

def main():
    if len(argv) <= 1:
        print('Enter some argv')
        return
    date = argv[1]
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
    searcher = Searcher(connection=conn)
    # pars = searcher.by_date(date, technopark_auditoriums, searcher.create_minimal_pair)
    # for p in pars:
    #     print(p)
    pars = searcher.by_date(date, technopark_auditoriums, searcher.create_pair_with_date_and_time)
    for p in pars:
        print(p)
    
    close_connection(conn)

if __name__=='__main__':
    main()