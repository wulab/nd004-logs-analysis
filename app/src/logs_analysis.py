#!/usr/bin/env python
#
# logs_analysis.py -- create a reporting tool that prints out reports
#

from datetime import datetime
import psycopg2
import sys
import time


def connect(attempt=0):
    '''Connects to the PostgreSQL database. Returns a database connection.'''
    if attempt > 2:
        sys.exit('  ! Failed to connect to "news" database on host "db"\n')
    else:
        try:
            return psycopg2.connect(host='db',
                                    dbname='news',
                                    user='vagrant',
                                    password='mysecretpassword')
        except psycopg2.OperationalError:
            time.sleep(5)
            return connect(attempt + 1)


def fetchall(query):
    '''Connects and queries the database, obtain data, then close communication.
    Returns a query result as a list of tuples.
    '''
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def report(question, answer):
    '''Formats and prints question and answer strings.'''
    print( '\n{0}\n\nAnswer:\n\n{1}'.format(question, answer) )


def print_most_popular_articles():
    '''Prints the most popular three articles of all time.'''
    question = '1. What are the most popular three articles of all time?'
    answer = ''
    query = '''\
        SELECT articles.title,
                count(*) AS views
        FROM articles,
                log
        WHERE log.path = concat('/article/', articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;
        '''

    for row in fetchall(query):
        answer += '  "{0}" — {1} views\n'.format(*row)

    report(question=question, answer=answer)


def print_most_popular_authors():
    '''Sums up all of the articles each author has written,
    and prints out authors who get the most page views.
    '''
    question = '2. Who are the most popular article authors of all time?'
    answer = ''
    query = '''\
        SELECT authors.name,
               count(*) AS views
        FROM authors,
             articles,
             log
        WHERE authors.id = articles.author
          AND log.path = concat('/article/', articles.slug)
        GROUP BY authors.name
        ORDER BY views DESC;
        '''

    for row in fetchall(query):
        answer += '  "{0}" — {1} views\n'.format(*row)

    report(question=question, answer=answer)


def print_error_reporting():
    '''Sums up all of the articles each author has written,
    and prints out authors who get the most page views.
    '''
    question = '3. On which days did more than 1% of requests lead to errors?'
    answer = ''
    query = '''\
        SELECT time::date AS date,
               count(NULLIF(status, '200 OK')) / count(*)::decimal AS errors
        FROM log
        GROUP BY date
        HAVING count(NULLIF(status, '200 OK')) / count(*)::decimal > 0.01
        ORDER BY date;
        '''

    for row in fetchall(query):
        date = datetime.strptime(str(row[0]), '%Y-%m-%d')
        answer += '  {0:%B %d, %Y} — {1:.2%} errors\n'.format(date, row[1])

    report(question=question, answer=answer)


if __name__ == '__main__':
    print_most_popular_articles()
    print_most_popular_authors()
    print_error_reporting()
