#! /usr/bin/env python2.7

import psycopg2
import sys

the_mainstream_media = "dbname=news"


def find_most_popular_articles():
    "Return 3 articles which have been accessed the most in descending order"
    query =   '''select title as article, count (*) as views
                 from articles join log
                 on concat('/article/', articles.slug) = log.path
                 group by articles.title
                 order by views desc limit 3;'''
    best_clickbait = get_query_results(query)
    return best_clickbait


def find_most_popular_authors():
    "Return the authors who get the most views in descending order"
    query =   '''select authors.name as author, count(*) as views
                 from authors join articles on authors.id = articles.author
                 join log on concat('/article/', articles.slug) = log.path
                 group by authors.name order by views desc;'''
    buzzfeed = get_query_results(query)
    return buzzfeed


def find_error_days():
    "Return the days on which more than 1 percent of requests led to errors"
    # Make sure you've created both views as instructed in README.md
    query =   '''select pct_err.* from (
                 select reqs_per_day.day,
                 round((err_per_day.errors * 100.00 / reqs_per_day.reqs), 2)
                 as pct_errors
                 from err_per_day join reqs_per_day
                 on err_per_day.day = reqs_per_day.day) pct_err
                 where pct_errors > 1.00;'''
    disaster_days = get_query_results(query)
    return disaster_days

def get_query_results(query):
    conn = psycopg2.connect(the_mainstream_media)
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result

if __name__ == '__main__':
    loganalysis = open('logs-analysis.txt', 'w')
    loganalysis.write(str(find_most_popular_articles()) + '\n')
    loganalysis.write(str(find_most_popular_authors()) + '\n')
    loganalysis.write(str(find_error_days()) + '\n')
    loganalysis.close()
