#! /usr/bin/env python2.7

import psycopg2
import sys

the_mainstream_media = "news"


def find_most_popular_articles(analysisfile):
    "Return 3 articles which have been accessed the most in descending order"
    query = '''select title as article, count (*) as views
               from articles join log
               on concat('/article/', articles.slug) = log.path
               group by articles.title
               order by views desc limit 3;'''
    best_clickbait = get_query_results(query)
    analysisfile.write("\nWhat are the top 3 articles of all time?\n")
    for title, views in best_clickbait:
        analysisfile.write("   {} -- {} views\n".format(title, views))


def find_most_popular_authors(analysisfile):
    "Return the authors who get the most views in descending order"
    query = '''select authors.name as author, count(*) as views
               from authors join articles on authors.id = articles.author
               join log on concat('/article/', articles.slug) = log.path
               group by authors.name order by views desc;'''
    buzzfeed = get_query_results(query)
    analysisfile.write("\nWho are the most popular authors?\n")
    for author, views in buzzfeed:
        analysisfile.write("   {} -- {} views\n".format(author, views))


def find_error_days(analysisfile):
    "Return the days on which more than 1 percent of requests led to errors"
    # Make sure you've created both views as instructed in README.md
    query = '''select pct_err.day, pct_err.pct_errors from (
               select reqs_per_day.day,
               round((err_per_day.errors * 100.00 / reqs_per_day.reqs), 2)
               as pct_errors
               from err_per_day join reqs_per_day
               on err_per_day.day = reqs_per_day.day) pct_err
               where pct_errors > 1.00;'''
    disaster_days = get_query_results(query)
    analysisfile.write("\nWhen did more than 1 pct of requests give errors?\n")
    for day, pct_errors in disaster_days:
        analysisfile.write("   {} -- {} pct errors\n".format(day, pct_errors))


def connect_to_db(db_name = "news"):
    "Connect to the PostgreSQL database, returns database connection and cursor"
    try:
        conn = psycopg2.connect("dbname={}".format(db_name))
        c = conn.cursor()
        return conn, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)


def get_query_results(query):
    "Execute query using cursor from connect_to_db() method"
    conn, c = connect_to_db(the_mainstream_media)
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

if __name__ == '__main__':
    loganalysis = open('logs-analysis.txt', 'w')
    find_most_popular_articles(loganalysis)
    find_most_popular_authors(loganalysis)
    find_error_days(loganalysis)
    loganalysis.close()
