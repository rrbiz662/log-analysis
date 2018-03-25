import psycopg2


def get_top_articles(cur, order, limit):
    """Fetches the top articles.

    Fetches the number of top articles in the specified
    order.

    Args:
        cur(object): The cursor to execute the query.
        order(str): The order to view the rows in.
        limit(int): The number of rows to view.
    """
    cur.execute(
                "SELECT articles.title, COUNT(*) as views"
                " FROM log, articles"
                " WHERE log.path LIKE '%'||articles.slug AND"
                " log.method = 'GET'"
                " GROUP BY articles.title"
                " ORDER BY views {}"
                " LIMIT {};".format(order, limit))

    rows = cur.fetchall()
    file = open("top_articles_report.txt", "w")
    for row in rows:
        file.write("\"{}\" - {} views \n".format(row[0], row[1]))

    file.close()


def get_top_authors(cur, order):
    """Fetches the top authors.

    Args:
        cur(object): The cursor to execute the query.
        order(str): The order to view the rows in.
    """
    cur.execute(
                "SELECT authors.name, COUNT(*) as views"
                " FROM authors, articles, log"
                " WHERE authors.id = articles.author AND"
                " log.path LIKE '%'||articles.slug AND"
                " log.method = 'GET'"
                " GROUP BY authors.name"
                " ORDER BY views {}".format(order))

    rows = cur.fetchall()
    file = open("top_authors_report.txt", "w")
    for row in rows:
        file.write("{} - {} views \n".format(row[0], row[1]))

    file.close()


def get_error_days(cur, error_percent):
    """Fetches the days in which requests led to errors.

    Fetches the days in which the specified percentage
    of requests led to errors.

    Args:
        cur(object): The cursor to execute the query.
        error_percent(int): The percentage of requests that led to errors.
    """
    cur.execute(
                "SELECT to_char(log_errors.date, 'Mon DD YYYY'),"
                " round((log_errors.errors * 100"
                " / log_requests.total::numeric), 2) as percent"
                " FROM log_errors, log_requests"
                " WHERE log_errors.date = log_requests.date AND"
                " log_errors.errors * 100 / log_requests.total::numeric > {}"
                " ORDER BY log_errors.date".format(error_percent))

    rows = cur.fetchall()
    file = open("error_report.txt", "w")
    for row in rows:
        file.write("{} - {}% errors \n".format(row[0], row[1]))

    file.close()


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
        get_top_articles(cur, "DESC", 3)
        get_top_authors(cur, "DESC")
        get_error_days(cur, 1)
        conn.close()
        print("Successful creating reports.")

main()
