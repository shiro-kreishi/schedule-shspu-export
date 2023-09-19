import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection(
        db='postgres', user='postgres', 
        password='postgres', host='localhost', port=5432):
    return psycopg2.connect(
    database='sch', user='obs',
    password='dideboki', host='shebot.shgpi', port=5432 
)

def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def execute_sql(sql: str, cur, all=False):
    cur.execute(sql)
    if all:
        return cur.fetchall()
    return cur.fetchone()

def close_connection(conn):
    return conn.close()
