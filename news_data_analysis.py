#!/usr/bin/env python3
import psycopg2
from psycopg2 import sql


def get_top_articles(cur, limit):
    """Fetches the top articles.

    Fetches the number of top articles in the specified
    order.

    Args:
        cur(obj): The cursor to execute the query.
        limit(int): The number of rows to view.

    Return:
        True if success, False otherwise.
    """
    data = (limit, )
    query = '''SELECT articles.title, COUNT(*) as views
            FROM log, articles
            WHERE log.path = '/article/'||articles.slug AND
            log.method = 'GET'
            GROUP BY articles.title
            ORDER BY views DESC
            LIMIT %s'''
    rows = get_data(cur, query, data)

    # Write data to txt file.
    if rows is not None:
        file = open("top_articles_report.txt", "w")
        for row in rows:
            file.write("\"{}\" - {} views \n".format(row[0], row[1]))
        file.close()

        return True
    else:
        return False


def get_top_authors(cur):
    """Fetches the top authors.

    Args:
        cur(obj): The cursor to execute the query.

    Return:
        True if success, False otherwise.
    """
    data = ()
    query = '''SELECT authors.name, COUNT(*) as views
            FROM authors, articles, log
            WHERE authors.id = articles.author AND
            log.path = '/article/'||articles.slug AND
            log.method = 'GET'
            GROUP BY authors.name
            ORDER BY COUNT(*) DESC'''
    rows = get_data(cur, query, data)

    # Write data to txt file.
    if rows is not None:
        file = open("top_authors_report.txt", "w")
        for row in rows:
            file.write("{} - {} views \n".format(row[0], row[1]))
        file.close()

        return True
    else:
        return False


def get_error_days(cur, error_percent):
    """Fetches the days in which requests led to errors.

    Fetches the days in which the specified percentage
    of requests led to errors.

    Args:
        cur(obj): The cursor to execute the query.
        error_percent(int): The percentage of requests that led to errors.

    Return:
        True if success, False otherwise.
    """
    data = (error_percent, )
    query = '''SELECT to_char(log_errors.date, 'Mon DD YYYY'),
            round((log_errors.errors * 100
            / log_requests.total::numeric), 2) as percent
            FROM log_errors, log_requests
            WHERE log_errors.date = log_requests.date AND
            log_errors.errors * 100
            / log_requests.total::numeric > %s
            ORDER BY log_errors.date'''
    rows = get_data(cur, query, data)

    # Write data to txt file.
    if rows is not None:
        file = open("error_report.txt", "w")
        for row in rows:
            file.write("{} - {}% errors \n".format(row[0], row[1]))
        file.close()

        return True
    else:
        return False


def get_data(cur, query, data):
    """Fetches the data specified in the query.

    Args:
        cur(obj): The cursor to execute the query.
        query(str): The query to execute.
        data(tuple): The values to insert into the query.

    Return:
        The data or None if there is an error.
    """
    try:
        cur.execute(query, data)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(e)
        cur.connection.rollback()
        return None


def setup_connection(db_name):
    """Sets up the database connection.

    Sets up a Postgre database connection with passed in
    database's name.

    Args:
        db_name(str): The name of the database to connect to.

    Returns:
        A cursor to the database.
    """
    try:
        return psycopg2.connect(dbname=db_name)
    except psycopg2.Error as e:
        print(e)


def main():
    """Main function to run the code."""
    conn = setup_connection("news")

    if conn is not None:
        cur = conn.cursor()
        # Create top articles report.
        if get_top_articles(cur, 3):
            print("Successful creating top articles report.")
        else:
            print("Error creating top articles report.")
        # Create top authors report.
        if get_top_authors(cur):
            print("Successful creating top authors report.")
        else:
            print("Error creating top authors report.")
        # Create error report.
        if get_error_days(cur, 1):
            print("Successful creating daily error percentage report.")
        else:
            print("Error creating daily error percentage report.")

        conn.close()

if __name__ == '__main__':
    main()
