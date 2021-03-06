import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops all pre-defined tables in the current connection.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates all pre-defined tables in the current connection.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Parse AWS config and creating necessary tables for analysis.
    """
    config = configparser.ConfigParser()
    config.read('dwh_local.cfg')
    conn = psycopg2.connect("host={} dbname={} user={} password={} "
                            "port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
